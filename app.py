import os
import csv
import io
import urllib.parse
import math
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response # <-- Swapped StreamingResponse for Response
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import get_db_connection
from dotenv import load_dotenv

# Load hidden variables from .env
load_dotenv()

app = FastAPI(title="Pestong Yummy PH System")

# Add SessionMiddleware to remember logged-in users. 
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY', 'secret'))

templates = Jinja2Templates(directory="templates")


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def log_audit(username, action_type, description):
    """Helper function to record actions in the audit log table."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO audit_log (username, action_type, description)
        VALUES (%s, %s, %s)
    """, (username, action_type, description))
    db.commit()
    db.close()

@app.on_event("startup")
def startup_event():
    db = get_db_connection()
    if db:
        print("🌿 SUCCESS: Connected to the Pestong Yummy database!")
        db.close()
    else:
        print("❌ ERROR: Could not connect to the database. Please check your .env file.")

def generate_dss_insights(cursor):
    """
    Internal Expert System to replace the external AI API.
    It calculates how fast items are selling and predicts stockouts.
    """
    try:
        # Look at sales from the last 7 days
        cursor.execute("""
            SELECT p.name, p.current_stock_jars, 
                   COALESCE(SUM(oi.quantity), 0) as sold_last_7_days
            FROM products p
            LEFT JOIN order_items oi ON p.id = oi.product_id
            LEFT JOIN orders o ON oi.order_id = o.id AND o.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY p.id
        """)
        product_stats = cursor.fetchall()
        
        insights = []
        for stat in product_stats:
            # FIX: Force MySQL Data to become standard Python numbers
            sold = float(stat['sold_last_7_days'] or 0)
            stock = int(stat['current_stock_jars'] or 0)
            name = stat['name']
            
            daily_velocity = sold / 7.0
            
            if stock == 0:
                insights.append({"type": "critical", "message": f"STOCKOUT: {name} is completely out of stock. Halting sales."})
            elif daily_velocity > 0:
                days_remaining = stock / daily_velocity
                if days_remaining <= 3:
                    insights.append({"type": "warning", "message": f"URGENT: {name} is selling fast. Stock will deplete in about {int(days_remaining)} days. Produce more today."})
                elif days_remaining > 14:
                    insights.append({"type": "info", "message": f"OVERSTOCK: {name} is moving slowly. Consider running a weekend promotion."})
            else:
                insights.append({"type": "info", "message": f"NO MOVEMENT: {name} hasn't sold in 7 days. Check marketing."})
                
        return insights
        
    except Exception as e:
        # SAFETY NET: If the math fails, print the error to the terminal but don't crash the website!
        print(f"DSS Error: {e}")
        return [{"type": "info", "message": "DSS System is calibrating data..."}]

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Shows the login screen."""
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
async def handle_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handles secure login and records it in the login_history table."""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Grab the user's IP address
    client_ip = request.client.host if request.client else "Unknown"
    
    cursor.execute("SELECT * FROM users WHERE username = %s AND status = 'active'", (username,))
    user = cursor.fetchone()

    if user and user['password_hash'] == password:
        # Success! Set the session
        request.session['user_id'] = user['id']
        request.session['username'] = user['username']
        request.session['role'] = user['role']
        
        # Record successful login
        cursor.execute("INSERT INTO login_history (username, action, ip_address) VALUES (%s, 'login', %s)", (user['username'], client_ip))
        db.commit()
        db.close()
        
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        # Record failed attempt
        cursor.execute("INSERT INTO login_history (username, action, ip_address) VALUES (%s, 'failed_attempt', %s)", (username, client_ip))
        db.commit()
        db.close()
        
        return templates.TemplateResponse(request, "login.html", {"error": "Invalid username or password"})

@app.get("/logout")
async def logout_user(request: Request):
    """Securely destroys the user session and logs them out."""
    db = get_db_connection()
    cursor = db.cursor()
    
    username = request.session.get('username', 'Unknown')
    client_ip = request.client.host if request.client else "Unknown"
    
    # Record the logout
    cursor.execute("INSERT INTO login_history (username, action, ip_address) VALUES (%s, 'logout', %s)", (username, client_ip))
    db.commit()
    db.close()
    
    # This completely deletes their secure session!
    request.session.clear() 
    return RedirectResponse(url="/", status_code=303)

# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Shows the dashboard with KPI metrics and inventory alerts."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Fetch Ingredients for Low Stock Alerts
    cursor.execute("SELECT * FROM ingredients")
    ingredients_data = cursor.fetchall()
    
    # 2. KPI: Today's Revenue
    # CURDATE() is a MySQL command that only grabs data from today!
    cursor.execute("SELECT SUM(total_price) as today_revenue FROM orders WHERE DATE(created_at) = CURDATE()")
    today_revenue = cursor.fetchone()['today_revenue'] or 0.0
    
    # 3. KPI: Pending Orders
    cursor.execute("SELECT COUNT(id) as pending_count FROM orders WHERE status = 'pending'")
    pending_orders = cursor.fetchone()['pending_count'] or 0
    
    # 4. KPI: Total Finished Jars on Shelf
    cursor.execute("SELECT SUM(current_stock_jars) as total_jars FROM products")
    total_jars = cursor.fetchone()['total_jars'] or 0
    
    # Generate our internal AI insights!
    business_insights = generate_dss_insights(cursor)
    
    db.close()
        
    return templates.TemplateResponse(request, "dashboard.html", {
        "username": request.session.get('username'),
        "role": request.session.get('role'),
        "ingredients": ingredients_data,
        "today_revenue": today_revenue,
        "pending_orders": pending_orders,
        "total_jars": int(total_jars),
        "insights": business_insights  # <-- ADD THIS LINE
    })

# ==========================================
# ORDERS ROUTES (Multi-Item & Pagination)
# ==========================================

@app.get("/orders", response_class=HTMLResponse)
async def view_orders(request: Request, error: str = None, success: str = None):
    # Security check for appropriate roles
    current_role = request.session.get('role')
    if 'username' not in request.session or current_role not in ['admin', 'coordinator']:
        return RedirectResponse(url="/dashboard", status_code=303)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Fetch products for the Create Order pop-up form
    cursor.execute("SELECT id, name, price, current_stock_jars FROM products")
    products_data = cursor.fetchall()
    
    # 2. Fetch the recent sales history for the main table
    cursor.execute("""
        SELECT id, customer_name, total_price, payment_method, payment_status, status, created_at 
        FROM orders 
        ORDER BY created_at DESC 
        LIMIT 20
    """)
    recent_orders = cursor.fetchall()
    
    db.close()
    return templates.TemplateResponse(request, "orders.html", {
        "request": request,
        "products": products_data,
        "recent_orders": recent_orders,
        "error": error,
        "success": success
    })

@app.post("/orders")
async def create_order(request: Request):
    """Handles new multi-item orders with Stock Validation."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    form_data = await request.form()
    customer_name = form_data.get('customer_name')
    payment_method = form_data.get('payment_method')
    payment_status = form_data.get('payment_status')
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Fetch current prices and stock to prepare the order
    cursor.execute("SELECT id, price, name, current_stock_jars FROM products")
    db_products = cursor.fetchall()
    
    items_to_buy = []
    total_order_price = 0.0
    
    # 2. Map form quantities to items
    for product in db_products:
        qty_str = form_data.get(f"product_qty_{product['id']}")
        if qty_str and int(qty_str) > 0:
            qty = int(qty_str)
            
            # --- START VALIDATION BLOCK ---
            # Check if current stock is enough for this specific item
            if product['current_stock_jars'] < qty:
                db.close()
                error_msg = f"Stock Shortage: '{product['name']}' only has {product['current_stock_jars']} left, but you requested {qty}."
                return RedirectResponse(url=f"/orders?error={error_msg}", status_code=303)
            # --- END VALIDATION BLOCK ---

            subtotal = qty * float(product['price'])
            total_order_price += subtotal
            items_to_buy.append({
                "product_id": product['id'],
                "name": product['name'],
                "quantity": qty,
                "subtotal": subtotal
            })
            
    if not items_to_buy:
        db.close()
        return RedirectResponse(url="/orders", status_code=303)
        
    # 3. Create the Parent Order
    cursor.execute("""
        INSERT INTO orders (customer_name, total_price, payment_method, payment_status, status)
        VALUES (%s, %s, %s, %s, 'pending')
    """, (customer_name, total_order_price, payment_method, payment_status))
    
    new_order_id = cursor.lastrowid
    
    # 4. Create the Child Items and Deduct Jars from Shelf
    item_descriptions = []
    for item in items_to_buy:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, subtotal)
            VALUES (%s, %s, %s, %s)
        """, (new_order_id, item['product_id'], item['quantity'], item['subtotal']))
        
        cursor.execute("UPDATE products SET current_stock_jars = current_stock_jars - %s WHERE id = %s", (item['quantity'], item['product_id']))
        item_descriptions.append(f"{item['quantity']}x {item['name']}")
        
    # 5. Log it to the Audit Trail!
    current_user = request.session.get('username')
    desc_str = ", ".join(item_descriptions)
    log_audit(current_user, "SALE", f"Order #{new_order_id} created for {customer_name}. Total: ₱{total_order_price}. Items: {desc_str}.")
    
    db.commit()
    db.close()
    return RedirectResponse(url="/orders?success=Order successfully placed!", status_code=303)

@app.post("/orders/update")
async def update_order(request: Request):
    """Updates BOTH the payment status and the order workflow status simultaneously."""
    role = request.session.get('role')
    if role not in ['admin', 'coordinator']:
        return RedirectResponse(url="/orders", status_code=303)

    form_data = await request.form()
    order_id = form_data.get('order_id')
    new_status = form_data.get('new_status')
    payment_status = form_data.get('payment_status')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
    current_order = cursor.fetchone()

    if new_status == 'cancelled' and current_order['status'] != 'cancelled':
        cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id = %s", (order_id,))
        items = cursor.fetchall()
        
        for item in items:
            cursor.execute("""
                UPDATE products
                SET current_stock_jars = current_stock_jars + %s
                WHERE id = %s
            """, (item['quantity'], item['product_id']))
            
        log_audit(request.session.get('username'), "UNDO", f"Cancelled Order #{order_id} and returned items to stock.")

    cursor.execute("UPDATE orders SET status = %s, payment_status = %s WHERE id = %s", (new_status, payment_status, order_id))

    db.commit()
    db.close()
    return RedirectResponse(url="/orders?success=Order status updated successfully!", status_code=303)


# ==========================================
# PRODUCTION & SCHEDULE ROUTES
# ==========================================

import math

@app.get("/production", response_class=HTMLResponse)
async def production_page(request: Request, error: str = None, success: str = None):
    """Shows production capabilities and the button to log a new batch."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Fetch products and calculate max possible jars based on inventory
    cursor.execute("SELECT id, name, current_stock_jars, price FROM products")
    products_data = cursor.fetchall()
    
    for product in products_data:
        cursor.execute("SELECT ingredient_id, amount_needed FROM recipes WHERE product_id = %s", (product['id'],))
        recipe_items = cursor.fetchall()
        max_jars = float('inf')
        
        if not recipe_items:
            max_jars = 0 
        else:
            for item in recipe_items:
                cursor.execute("SELECT current_stock_usage FROM ingredients WHERE id = %s", (item['ingredient_id'],))
                ing = cursor.fetchone()
                if ing and item['amount_needed'] > 0:
                    possible = int(ing['current_stock_usage'] // item['amount_needed'])
                    if possible < max_jars:
                        max_jars = possible
                        
        product['max_possible'] = max_jars if max_jars != float('inf') else 0
        
    db.close()
    
    return templates.TemplateResponse(request, "production.html", {
        "products": products_data,
        "role": request.session.get('role'),
        "error": error,      
        "success": success   
    })

@app.post("/production")
async def log_production(
    request: Request,
    product_id: int = Form(...),
    jars_produced: int = Form(...)
):
    """Validates stock, deducts ingredients, and forces status to In Progress."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT ingredient_id, amount_needed FROM recipes WHERE product_id = %s", (product_id,))
    recipe_items = cursor.fetchall()
    
    # 1. VALIDATION
    for item in recipe_items:
        cursor.execute("SELECT name, current_stock_usage FROM ingredients WHERE id = %s", (item['ingredient_id'],))
        ing = cursor.fetchone()
        amount_needed_total = item['amount_needed'] * jars_produced
        
        if ing['current_stock_usage'] < amount_needed_total:
            db.close()
            return RedirectResponse(url=f"/production?error=Action Blocked: Not enough {ing['name']} to make {jars_produced} jars.", status_code=303)
            
    # 2. DEDUCTION
    for item in recipe_items:
        amount_to_deduct = item['amount_needed'] * jars_produced
        cursor.execute("""
            UPDATE ingredients SET current_stock_usage = current_stock_usage - %s WHERE id = %s
        """, (amount_to_deduct, item['ingredient_id']))
        
    # 3. Log the batch (Forces it to 'in_progress')
    forced_status = 'in_progress'
    cursor.execute("""
        INSERT INTO production_batches (product_id, jars_produced, status) VALUES (%s, %s, %s)
    """, (product_id, jars_produced, forced_status))
    
    current_user = request.session.get('username')
    log_audit(current_user, "PRODUCTION", f"Started batch of {jars_produced} jars.")
    
    db.commit()
    db.close()
    
    # Send them a success message and remind them to check the Schedule page!
    return RedirectResponse(url="/production?success=Batch started! Ingredients deducted. Check the Schedule page to track it.", status_code=303)

@app.get("/schedule", response_class=HTMLResponse)
async def schedule_page(request: Request, error: str = None, success: str = None):
    """Shows the Work In Progress and Completed batches."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Fetch WIP History
    cursor.execute("""
        SELECT pb.id, pb.created_at, p.name as product_name, pb.jars_produced, pb.status, pb.product_id
        FROM production_batches pb
        JOIN products p ON pb.product_id = p.id
        WHERE pb.status = 'in_progress'
        ORDER BY pb.created_at DESC
    """)
    wip_data = cursor.fetchall()

    # Fetch Completed History
    cursor.execute("""
        SELECT pb.id, pb.created_at, p.name as product_name, pb.jars_produced, pb.status, pb.product_id
        FROM production_batches pb
        JOIN products p ON pb.product_id = p.id
        WHERE pb.status = 'completed'
        ORDER BY pb.created_at DESC LIMIT 30
    """)
    completed_data = cursor.fetchall()

    db.close()
    
    return templates.TemplateResponse(request, "schedule.html", {
        "wip_batches": wip_data,
        "completed_batches": completed_data,
        "role": request.session.get('role'),
        "error": error,      
        "success": success   
    })

@app.post("/production/update")
async def update_production_status(request: Request, batch_id: int = Form(...)):
    """Automatically marks a batch as Completed and adds it to the shelf."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM production_batches WHERE id = %s AND status = 'in_progress'", (batch_id,))
    batch = cursor.fetchone()
    
    if batch:
        # Add the jars to the shelf
        cursor.execute("UPDATE products SET current_stock_jars = current_stock_jars + %s WHERE id = %s", (batch['jars_produced'], batch['product_id']))
        
        # Change status to completed
        cursor.execute("UPDATE production_batches SET status = 'completed' WHERE id = %s", (batch_id,))
        
        log_audit(request.session.get('username'), "PRODUCTION", f"Batch #{batch_id} marked Completed. Jars added to shelf.")
        db.commit()
        
    db.close()
    
    # Redirect back to the SCHEDULE page where they clicked the button!
    return RedirectResponse(url="/schedule?success=Batch marked as Completed! Jars added to inventory.", status_code=303)


# ==========================================
# INVENTORY ROUTES (With Cost Tracking & Pagination)
# ==========================================

@app.get("/inventory", response_class=HTMLResponse)
async def inventory_page(request: Request, page: int = 1):
    """Shows current inventory status and paginated purchase history."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Fetch current stock (Left Side)
    cursor.execute("SELECT * FROM ingredients")
    ingredients_data = cursor.fetchall()
    
    # 2. Pagination Math (Reduced to 6 items to eliminate vertical scrolling!)
    records_per_page = 6
    offset = (page - 1) * records_per_page
    
    cursor.execute("SELECT COUNT(*) as total FROM ingredient_purchases")
    total_records = cursor.fetchone()['total']
    total_pages = (total_records + records_per_page - 1) // records_per_page
    if total_pages == 0:
        total_pages = 1
    
    # 3. Fetch the exact 6 records for the current page (Right Side)
    cursor.execute("""
        SELECT ip.id, ip.created_at, i.name as ingredient_name, 
               ip.purchase_amount, i.purchase_unit, ip.cost 
        FROM ingredient_purchases ip
        JOIN ingredients i ON ip.ingredient_id = i.id
        ORDER BY ip.created_at DESC 
        LIMIT %s OFFSET %s
    """, (records_per_page, offset))
    history_data = cursor.fetchall()
    
    db.close()
    
    return templates.TemplateResponse(request, "inventory.html", {
        "ingredients": ingredients_data,
        "history": history_data,
        "role": request.session.get('role'),
        "current_page": page,
        "total_pages": total_pages
    })

@app.post("/inventory/purchase")
async def log_purchase(
    request: Request,
    ingredient_id: int = Form(...),
    purchase_amount: float = Form(...),
    cost: float = Form(...)
):
    """Exclusively handles financial market purchases."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT name, conversion_factor, purchase_unit, usage_unit FROM ingredients WHERE id = %s", (ingredient_id,))
    ingredient = cursor.fetchone()
    
    if ingredient:
        added_usage_amount = purchase_amount * float(ingredient['conversion_factor'])
        
        # Add to the pantry
        cursor.execute("UPDATE ingredients SET current_stock_usage = current_stock_usage + %s WHERE id = %s", (added_usage_amount, ingredient_id))
        
        # Log as a purchase
        cursor.execute("""
            INSERT INTO ingredient_purchases (ingredient_id, purchase_amount, cost, restock_type)
            VALUES (%s, %s, %s, 'purchase')
        """, (ingredient_id, purchase_amount, cost))
        
        log_audit(request.session.get('username'), "RESTOCK", f"Purchased {purchase_amount} {ingredient['purchase_unit']} of {ingredient['name']} for ₱{cost}.")
        db.commit()
        
    db.close()
    return RedirectResponse(url="/inventory", status_code=303)


# ==========================================
# AUDIT TRAIL ROUTE
# ==========================================

@app.get("/audit", response_class=HTMLResponse)
async def audit_page(request: Request, page: int = 1):
    """Shows the permanent history with pagination to handle massive data."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Setup Pagination Math (50 records per page)
    records_per_page = 50
    offset = (page - 1) * records_per_page
    
    # 2. Find out exactly how many total pages of Activity Logs we have
    cursor.execute("SELECT COUNT(*) as total FROM audit_log")
    total_logs = cursor.fetchone()['total']
    
    # This formula rounds up. If we have 51 records, it gives us 2 pages.
    total_pages = (total_logs + records_per_page - 1) // records_per_page 
    if total_pages == 0:
        total_pages = 1 # Always show at least page 1
    
    # 3. Fetch ONLY the 50 records for the current page
    cursor.execute("SELECT * FROM audit_log ORDER BY created_at DESC LIMIT %s OFFSET %s", (records_per_page, offset))
    logs_data = cursor.fetchall()
    
    # 4. Fetch the recent Login History (We'll keep this at a fixed 50 limit for simplicity on the side panel)
    cursor.execute("SELECT * FROM login_history ORDER BY created_at DESC LIMIT 50")
    logins_data = cursor.fetchall()
    
    db.close()
    
    return templates.TemplateResponse(request, "audit.html", {
        "logs": logs_data,
        "logins": logins_data,
        "current_page": page,
        "total_pages": total_pages
    })

# ==========================================
# HARVEST LOG ROUTES
# ==========================================

@app.get("/harvest", response_class=HTMLResponse)
async def harvest_page(request: Request):
    """Loads the dedicated Harvest page, showing only farmable herbs."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Only fetch the herbs for the harvest dropdown!
    cursor.execute("SELECT * FROM ingredients WHERE name IN ('Basil', 'Spinach', 'Malunggay', 'Mint')")
    herbs_data = cursor.fetchall()
    
    # Fetch harvest history
    cursor.execute("""
        SELECT ip.id, ip.created_at, i.name as ingredient_name, ip.purchase_amount as harvest_amount, i.purchase_unit 
        FROM ingredient_purchases ip
        JOIN ingredients i ON ip.ingredient_id = i.id
        WHERE ip.restock_type = 'harvest'
        ORDER BY ip.created_at DESC LIMIT 30
    """)
    harvest_history = cursor.fetchall()
    
    db.close()
    
    return templates.TemplateResponse(request, "harvest.html", {
        "herbs": herbs_data,
        "history": harvest_history,
        "role": request.session.get('role')
    })

@app.post("/harvest")
async def log_harvest(
    request: Request,
    ingredient_id: int = Form(...),
    harvest_amount: float = Form(...)
):
    """Adds harvested crops directly to the pantry with zero cost."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT name, conversion_factor, purchase_unit FROM ingredients WHERE id = %s", (ingredient_id,))
    ingredient = cursor.fetchone()
    
    if ingredient:
        added_usage_amount = harvest_amount * float(ingredient['conversion_factor'])
        
        # Add the fresh crops directly to the master pantry!
        cursor.execute("UPDATE ingredients SET current_stock_usage = current_stock_usage + %s WHERE id = %s", (added_usage_amount, ingredient_id))
        
        # Log it as a harvest with exactly ₱0.00 cost
        cursor.execute("""
            INSERT INTO ingredient_purchases (ingredient_id, purchase_amount, cost, restock_type)
            VALUES (%s, %s, 0.00, 'harvest')
        """, (ingredient_id, harvest_amount))
        
        log_audit(request.session.get('username'), "HARVEST", f"Harvested {harvest_amount} {ingredient['purchase_unit']} of {ingredient['name']}.")
        db.commit()
        
    db.close()
    return RedirectResponse(url="/harvest", status_code=303)

# ==========================================
# CUSTOMER PROFILES ROUTE (With Pagination)
# ==========================================

@app.get("/customers", response_class=HTMLResponse)
async def customers_page(request: Request, page: int = 1):
    """Shows customer profiles and their paginated order history."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Aggregate Customer Data (Leaderboard)
    cursor.execute("""
        SELECT 
            o.customer_name, 
            COUNT(DISTINCT o.id) as total_orders, 
            SUM(oi.quantity) as total_jars,
            SUM(oi.subtotal) as total_spent,
            MIN(o.created_at) as first_order_date
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        GROUP BY o.customer_name
        ORDER BY total_spent DESC
    """)
    customers_data = cursor.fetchall()
    
    # 2. Pagination Math for Recent Transactions (10 records per page)
    records_per_page = 10
    offset = (page - 1) * records_per_page
    
    cursor.execute("SELECT COUNT(*) as total FROM orders")
    total_orders = cursor.fetchone()['total']
    total_pages = (total_orders + records_per_page - 1) // records_per_page
    if total_pages == 0:
        total_pages = 1
    
    # 3. Get the paginated recent individual orders
    cursor.execute("""
        SELECT o.id, o.created_at, o.customer_name, o.total_price, o.payment_method,
               GROUP_CONCAT(CONCAT(oi.quantity, 'x ', p.name) SEPARATOR '<br>') as item_details
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        GROUP BY o.id
        ORDER BY o.created_at DESC
        LIMIT %s OFFSET %s
    """, (records_per_page, offset))
    recent_orders = cursor.fetchall()
    
    db.close()
    
    return templates.TemplateResponse(request, "customers.html", {
        "customers": customers_data,
        "orders": recent_orders,
        "current_page": page,
        "total_pages": total_pages
    })

# ==========================================
# BUSINESS REPORTS & EXPORT ROUTES
# ==========================================

@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    """Shows automated business reports adapted for multi-item orders."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Weekly Summary
    cursor.execute("""
        SELECT 
            CONCAT('Week ', WEEK(o.created_at)) AS period,
            COUNT(DISTINCT o.id) as total_orders,
            SUM(oi.quantity) as total_jars,
            SUM(oi.subtotal) as total_revenue
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        GROUP BY YEAR(o.created_at), WEEK(o.created_at)
        ORDER BY YEAR(o.created_at) DESC, WEEK(o.created_at) DESC
        LIMIT 10
    """)
    weekly_data = cursor.fetchall()
    
    # 2. Monthly Summary
    cursor.execute("""
        SELECT 
            DATE_FORMAT(o.created_at, '%M %Y') AS period,
            COUNT(DISTINCT o.id) as total_orders,
            SUM(oi.quantity) as total_jars,
            SUM(oi.subtotal) as total_revenue
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        GROUP BY YEAR(o.created_at), MONTH(o.created_at)
        ORDER BY YEAR(o.created_at) DESC, MONTH(o.created_at) DESC
        LIMIT 12
    """)
    monthly_data = cursor.fetchall()

    # 3. Payment Method Breakdown
    cursor.execute("""
        SELECT 
            o.payment_method,
            COUNT(DISTINCT o.id) as total_orders,
            SUM(oi.subtotal) as total_revenue
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        GROUP BY o.payment_method
        ORDER BY total_revenue DESC
    """)
    payment_data = cursor.fetchall()
    
    db.close()
    
    return templates.TemplateResponse(request, "reports.html", {
        "weekly": weekly_data,
        "monthly": monthly_data,
        "payments": payment_data
    })

@app.get("/reports/export")
async def export_sales_csv(request: Request):
    """Generates a downloadable CSV file of all multi-item sales."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Fetch all orders and string the items together with a " | " separator for Excel
    cursor.execute("""
        SELECT o.id, o.created_at, o.customer_name, 
               GROUP_CONCAT(CONCAT(oi.quantity, 'x ', p.name) SEPARATOR ' | ') as item_details,
               SUM(oi.quantity) as total_jars, o.total_price, o.payment_method, o.payment_status, o.status 
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        GROUP BY o.id
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Updated CSV Headers
    writer.writerow(['Order ID', 'Date', 'Customer Name', 'Items Purchased', 'Total Jars', 'Total Revenue (PHP)', 'Payment Method', 'Payment Status', 'Order Status'])

    for order in orders:
        writer.writerow([
            order['id'],
            order['created_at'].strftime('%Y-%m-%d %H:%M'),
            order['customer_name'],
            order['item_details'],
            order['total_jars'],
            order['total_price'],
            order['payment_method'],
            order['payment_status'],
            order['status']
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=Pestong_Yummy_Sales_Report.csv"}
    )

# ==========================================
# USER MANAGEMENT ROUTES (Admin Only)
# ==========================================

@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request, error: str = None, success: str = None):
    """Shows the user management page (Admin only)."""
    if 'username' not in request.session or request.session.get('role') != 'admin':
        return RedirectResponse(url="/dashboard", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Fetch all active users
    cursor.execute("SELECT id, username, full_name, role, created_at FROM users WHERE status = 'active'")
    users_data = cursor.fetchall()
    db.close()
    
    return templates.TemplateResponse(request, "users.html", {
        "request": request,  # Required for base.html session checks
        "users": users_data,
        "user_count": len(users_data),
        "current_user": request.session.get('username'),
        "error": error,      # NEW: Passes error to the Toast notification
        "success": success   # NEW: Passes success to the Toast notification
    })

@app.post("/users")
async def create_user(
    request: Request,
    username: str = Form(...),
    full_name: str = Form(...),
    role: str = Form(...),
    password: str = Form(...)
):
    """Creates a new user account if the limit hasn't been reached and the role is vacant."""
    if 'username' not in request.session or request.session.get('role') != 'admin':
        return RedirectResponse(url="/dashboard", status_code=303)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # --- NEW: BUSINESS RULE CONSTRAINT ---
    # Check if an active user already holds this exact role
    cursor.execute("SELECT full_name FROM users WHERE role = %s AND status = 'active'", (role,))
    existing_active_user = cursor.fetchone()

    if existing_active_user:
        db.close()
        # Format the error message and encode it for the URL
        raw_msg = f"Action blocked: {existing_active_user['full_name']} is currently the active {role}. Deactivate them first."
        error_msg = urllib.parse.quote(raw_msg)
        return RedirectResponse(url=f"/users?error={error_msg}", status_code=303)
    # --- END CONSTRAINT ---

    # Check if maximum employee limit is reached
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE status = 'active'")
    count_result = cursor.fetchone()
    
    if count_result['count'] < 4:
        cursor.execute("""
            INSERT INTO users (username, full_name, role, password_hash, status)
            VALUES (%s, %s, %s, %s, 'active')
        """, (username, full_name, role, password))
        
        current_user = request.session.get('username')
        log_audit(current_user, "SYSTEM", f"Created new {role} account for {full_name} ({username}).")
        
        db.commit()
        db.close()
        
        success_msg = urllib.parse.quote(f"Successfully added {full_name} as the new {role}.")
        return RedirectResponse(url=f"/users?success={success_msg}", status_code=303)
        
    db.close()
    
    # Trigger an error if they try to exceed the 4-user limit
    error_msg = urllib.parse.quote("Maximum limit of 4 active users reached.")
    return RedirectResponse(url=f"/users?error={error_msg}", status_code=303)

@app.post("/users/delete")
async def remove_user(request: Request, user_id: int = Form(...)):
    """Performs a 'Soft Delete' by deactivating the user."""
    # Security Check: Only Admins can do this
    if 'username' not in request.session or request.session.get('role') != 'admin':
        return RedirectResponse(url="/dashboard", status_code=303)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Find the user we are trying to delete
    cursor.execute("SELECT username, role FROM users WHERE id = %s", (user_id,))
    target_user = cursor.fetchone()
    
    # Safety Check: You cannot delete yourself!
    if target_user and target_user['username'] != request.session.get('username'):
        
        # Soft delete: Change status to inactive
        cursor.execute("UPDATE users SET status = 'inactive' WHERE id = %s", (user_id,))
        
        # Log this administrative action
        admin_username = request.session.get('username')
        log_audit(admin_username, "SYSTEM", f"Deactivated user account: {target_user['username']}.")
        
        db.commit()
        db.close()
        
        success_msg = urllib.parse.quote(f"User {target_user['username']} has been deactivated. The {target_user['role']} role is now vacant.")
        return RedirectResponse(url=f"/users?success={success_msg}", status_code=303)

    db.close()
    error_msg = urllib.parse.quote("You cannot delete your own admin account.")
    return RedirectResponse(url=f"/users?error={error_msg}", status_code=303)

# ==========================================
# AUDIT TRAIL ROUTE
# ==========================================

@app.get("/audit", response_class=HTMLResponse)
async def audit_page(request: Request):
    """Shows the permanent history of all stock movements and logins."""
    if 'username' not in request.session:
        return RedirectResponse(url="/", status_code=303)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Fetch general activity logs
    cursor.execute("SELECT * FROM audit_log ORDER BY created_at DESC LIMIT 100")
    logs_data = cursor.fetchall()
    
    # Fetch the new login history
    cursor.execute("SELECT * FROM login_history ORDER BY created_at DESC LIMIT 50")
    logins_data = cursor.fetchall()
    
    db.close()
    
    return templates.TemplateResponse(request, "audit.html", {
        "logs": logs_data,
        "logins": logins_data
    })