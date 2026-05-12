import os, csv, io, urllib.parse, math
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import get_db_connection
from dotenv import load_dotenv

# Load hidden variables from .env
load_dotenv()

# We add a nice title and description for the Swagger UI header!
app = FastAPI(
    title="Pestong Yummy PH - Management API",
    description="Internal Enterprise Dashboard API for Pestong Yummy operations, inventory, and sales.",
    version="1.0.0"
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY', 'secret'))
templates = Jinja2Templates(directory="templates")


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def log_audit(username, action_type, description):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO audit_log (username, action_type, description) VALUES (%s, %s, %s)", (username, action_type, description))
    db.commit()
    db.close()

@app.on_event("startup")
def startup_event():
    db = get_db_connection()
    if db:
        print("🌿 SUCCESS: Connected to the Pestong Yummy database!")
        db.close()

def generate_dss_insights(cursor):
    try:
        cursor.execute("""
            SELECT p.name, p.current_stock_jars, COALESCE(SUM(oi.quantity), 0) as sold_last_7_days
            FROM products p LEFT JOIN order_items oi ON p.id = oi.product_id
            LEFT JOIN orders o ON oi.order_id = o.id AND o.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) GROUP BY p.id
        """)
        insights = []
        for stat in cursor.fetchall():
            sold = float(stat['sold_last_7_days'] or 0)
            stock = int(stat['current_stock_jars'] or 0)
            name = stat['name']
            daily_velocity = sold / 7.0
            if stock == 0:
                insights.append({"type": "critical", "message": f"STOCKOUT: {name} completely out. Halt sales."})
            elif daily_velocity > 0:
                days_remaining = stock / daily_velocity
                if days_remaining <= 3: insights.append({"type": "warning", "message": f"URGENT: {name} low. {int(days_remaining)} days left."})
                elif days_remaining > 14: insights.append({"type": "info", "message": f"OVERSTOCK: {name} moving slowly."})
            else:
                insights.append({"type": "info", "message": f"NO MOVEMENT: {name} in 7 days."})
        return insights[:3] # Limit to top 3 insights for unscrollable view
    except Exception as e:
        return [{"type": "info", "message": "DSS System is calibrating data..."}]

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.get("/", response_class=HTMLResponse, tags=["🔐 Authentication"], summary="Show Login Page")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.post("/login", tags=["🔐 Authentication"], summary="Process User Login")
async def handle_login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    client_ip = request.client.host if request.client else "Unknown"
    cursor.execute("SELECT * FROM users WHERE username = %s AND status = 'active'", (username,))
    user = cursor.fetchone()
    if user and user['password_hash'] == password:
        request.session.update({'user_id': user['id'], 'username': user['username'], 'role': user['role']})
        cursor.execute("INSERT INTO login_history (username, action, ip_address) VALUES (%s, 'login', %s)", (user['username'], client_ip))
        db.commit()
        db.close()
        return RedirectResponse(url="/dashboard", status_code=303)
    cursor.execute("INSERT INTO login_history (username, action, ip_address) VALUES (%s, 'failed_attempt', %s)", (username, client_ip))
    db.commit()
    db.close()
    return templates.TemplateResponse(request, "login.html", {"error": "Invalid username or password"})

@app.get("/logout", tags=["🔐 Authentication"], summary="Securely Log Out User")
async def logout_user(request: Request):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO login_history (username, action, ip_address) VALUES (%s, 'logout', %s)", (request.session.get('username', 'Unknown'), request.client.host if request.client else "Unknown"))
    db.commit()
    db.close()
    request.session.clear() 
    return RedirectResponse(url="/", status_code=303)

# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.get("/dashboard", response_class=HTMLResponse, tags=["📊 Dashboard"], summary="View Role-Based Dashboard")
async def dashboard_page(request: Request):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    
    role = request.session.get('role')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    data = {"username": request.session.get('username'), "role": role}

    if role == 'admin':
        cursor.execute("SELECT * FROM ingredients")
        data['ingredients'] = cursor.fetchall()
        cursor.execute("SELECT SUM(total_price) as today_revenue FROM orders WHERE DATE(created_at) = CURDATE()")
        data['today_revenue'] = cursor.fetchone()['today_revenue'] or 0.0
        cursor.execute("SELECT COUNT(id) as pending_count FROM orders WHERE status = 'pending'")
        data['pending_orders'] = cursor.fetchone()['pending_count'] or 0
        cursor.execute("SELECT SUM(current_stock_jars) as total_jars FROM products")
        data['total_jars'] = int(cursor.fetchone()['total_jars'] or 0)
        data['insights'] = generate_dss_insights(cursor)
        cursor.execute("""
            SELECT p.name, SUM(oi.quantity) as total_sold 
            FROM order_items oi JOIN products p ON oi.product_id = p.id JOIN orders o ON oi.order_id = o.id 
            WHERE MONTH(o.created_at) = MONTH(CURDATE()) 
            GROUP BY p.id ORDER BY total_sold DESC LIMIT 1
        """)
        data['top_product'] = cursor.fetchone()
        cursor.execute("SELECT username, action_type, description, created_at FROM audit_log ORDER BY created_at DESC LIMIT 4")
        data['recent_activity'] = cursor.fetchall()

    elif role == 'coordinator':
        cursor.execute("SELECT COUNT(id) as pending_count FROM orders WHERE status = 'pending'")
        data['pending_orders'] = cursor.fetchone()['pending_count'] or 0
        cursor.execute("SELECT id, customer_name, total_price, payment_method, created_at FROM orders WHERE status = 'pending' ORDER BY created_at ASC LIMIT 4")
        data['urgent_orders'] = cursor.fetchall()
        cursor.execute("SELECT id, customer_name, total_price, created_at FROM orders WHERE status = 'completed' ORDER BY created_at DESC LIMIT 3")
        data['recent_completed'] = cursor.fetchall()

    elif role == 'packaging':
        cursor.execute("SELECT COUNT(*) as low_count FROM ingredients WHERE current_stock_usage <= low_stock_threshold")
        data['low_count'] = cursor.fetchone()['low_count'] or 0
        cursor.execute("SELECT * FROM ingredients WHERE current_stock_usage <= low_stock_threshold LIMIT 4")
        data['low_stock_alerts'] = cursor.fetchall()
        cursor.execute("SELECT i.name, ip.purchase_amount, i.purchase_unit, ip.restock_type, ip.created_at FROM ingredient_purchases ip JOIN ingredients i ON ip.ingredient_id = i.id ORDER BY ip.created_at DESC LIMIT 4")
        data['recent_restocks'] = cursor.fetchall()

    elif role == 'production':
        cursor.execute("SELECT name, current_stock_jars FROM products ORDER BY current_stock_jars ASC LIMIT 3")
        data['low_products'] = cursor.fetchall()
        cursor.execute("SELECT pb.id, p.name as product_name, pb.jars_produced, pb.created_at FROM production_batches pb JOIN products p ON pb.product_id = p.id WHERE pb.status = 'in_progress' ORDER BY pb.created_at ASC LIMIT 3")
        data['wip_batches'] = cursor.fetchall()
        cursor.execute("SELECT SUM(jars_produced) as daily_total FROM production_batches WHERE DATE(created_at) = CURDATE()")
        data['daily_jars'] = int(cursor.fetchone()['daily_total'] or 0)

    db.close()
    return templates.TemplateResponse(request, "dashboard.html", data)

# ==========================================
# ORDERS ROUTES 
# ==========================================

@app.get("/orders", response_class=HTMLResponse, tags=["🛒 Order Management"], summary="View Orders & Pending Queue")
async def view_orders(request: Request, page_p: int = 1, page_c: int = 1, error: str = None, success: str = None):
    if 'username' not in request.session or request.session.get('role') not in ['admin', 'coordinator']: return RedirectResponse(url="/dashboard", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price, current_stock_jars FROM products")
    products_data = cursor.fetchall()
    
    records_per_page = 10
    offset_p = (page_p - 1) * records_per_page
    offset_c = (page_c - 1) * records_per_page
    
    cursor.execute("SELECT COUNT(*) as total FROM orders WHERE status = 'pending'")
    total_pages_p = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    cursor.execute("SELECT id, customer_name, total_price, payment_method, payment_status, created_at FROM orders WHERE status = 'pending' ORDER BY created_at ASC LIMIT %s OFFSET %s", (records_per_page, offset_p))
    pending_orders = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM orders WHERE status = 'completed'")
    total_pages_c = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    cursor.execute("SELECT id, customer_name, total_price, payment_method, payment_status, created_at FROM orders WHERE status = 'completed' ORDER BY created_at DESC LIMIT %s OFFSET %s", (records_per_page, offset_c))
    completed_orders = cursor.fetchall()
    
    db.close()
    return templates.TemplateResponse(request, "orders.html", {
        "request": request, "products": products_data, "pending_orders": pending_orders, "completed_orders": completed_orders, 
        "error": error, "success": success, "current_page_p": page_p, "total_pages_p": total_pages_p,
        "current_page_c": page_c, "total_pages_c": total_pages_c, "per_page": records_per_page
    })

@app.post("/orders", tags=["🛒 Order Management"], summary="Create New Multi-Item Order")
async def create_order(request: Request):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    form_data = await request.form()
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, price, name, current_stock_jars FROM products")
    db_products = cursor.fetchall()
    
    items_to_buy, total_order_price = [], 0.0
    for product in db_products:
        qty_str = form_data.get(f"product_qty_{product['id']}")
        if qty_str and int(qty_str) > 0:
            qty = int(qty_str)
            if product['current_stock_jars'] < qty:
                db.close()
                return RedirectResponse(url=f"/orders?error=Stock Shortage: '{product['name']}' only has {product['current_stock_jars']} left.", status_code=303)
            subtotal = qty * float(product['price'])
            total_order_price += subtotal
            items_to_buy.append({"product_id": product['id'], "name": product['name'], "quantity": qty, "subtotal": subtotal})
            
    if not items_to_buy: db.close(); return RedirectResponse(url="/orders", status_code=303)
    
    cursor.execute("INSERT INTO orders (customer_name, total_price, payment_method, payment_status, status) VALUES (%s, %s, %s, %s, 'pending')", (form_data.get('customer_name'), total_order_price, form_data.get('payment_method'), form_data.get('payment_status')))
    new_order_id = cursor.lastrowid
    
    item_descriptions = []
    for item in items_to_buy:
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)", (new_order_id, item['product_id'], item['quantity'], item['subtotal']))
        cursor.execute("UPDATE products SET current_stock_jars = current_stock_jars - %s WHERE id = %s", (item['quantity'], item['product_id']))
        item_descriptions.append(f"{item['quantity']}x {item['name']}")
        
    log_audit(request.session.get('username'), "SALE", f"Order #{new_order_id} created for {form_data.get('customer_name')}. Total: ₱{total_order_price}. Items: {', '.join(item_descriptions)}.")
    db.commit()
    db.close()
    return RedirectResponse(url="/orders?success=Order successfully placed!", status_code=303)

@app.post("/orders/update", tags=["🛒 Order Management"], summary="Update Order Status (Complete/Cancel)")
async def update_order(request: Request):
    if request.session.get('role') not in ['admin', 'coordinator']: return RedirectResponse(url="/orders", status_code=303)
    
    form_data = await request.form()
    order_id = form_data.get('order_id')
    new_status = form_data.get('new_status')
    payment_status = form_data.get('payment_status')
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
    current_order = cursor.fetchone()
    
    if current_order and new_status == 'cancelled' and current_order['status'] != 'cancelled':
        cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id = %s", (order_id,))
        items = cursor.fetchall()
        for item in items:
            cursor.execute("UPDATE products SET current_stock_jars = current_stock_jars + %s WHERE id = %s", (item['quantity'], item['product_id']))
        log_audit(request.session.get('username'), "UNDO", f"Cancelled Order #{order_id} and returned items.")
        
    cursor.execute("UPDATE orders SET status = %s, payment_status = %s WHERE id = %s", (new_status, payment_status, order_id))
    db.commit()
    db.close()
    
    return RedirectResponse(url="/orders?success=Order updated!", status_code=303)

# ==========================================
# PRODUCTION & SCHEDULE ROUTES
# ==========================================

@app.get("/production", response_class=HTMLResponse, tags=["🏭 Production System"], summary="View Production Floor & Start Batches")
async def production_page(request: Request, error: str = None, success: str = None):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, current_stock_jars, price FROM products")
    products_data = cursor.fetchall()
    for product in products_data:
        cursor.execute("SELECT ingredient_id, amount_needed FROM recipes WHERE product_id = %s", (product['id'],))
        recipe_items = cursor.fetchall()
        max_jars = float('inf')
        if not recipe_items: max_jars = 0 
        else:
            for item in recipe_items:
                cursor.execute("SELECT current_stock_usage FROM ingredients WHERE id = %s", (item['ingredient_id'],))
                ing = cursor.fetchone()
                if ing and item['amount_needed'] > 0:
                    max_jars = min(max_jars, int(ing['current_stock_usage'] // item['amount_needed']))
        product['max_possible'] = max_jars if max_jars != float('inf') else 0
    db.close()
    return templates.TemplateResponse(request, "production.html", {"products": products_data[:4], "role": request.session.get('role'), "error": error, "success": success})

@app.post("/production", tags=["🏭 Production System"], summary="Log New Production Batch")
async def log_production(request: Request, product_id: int = Form(...), jars_produced: int = Form(...)):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT ingredient_id, amount_needed FROM recipes WHERE product_id = %s", (product_id,))
    recipe_items = cursor.fetchall()
    for item in recipe_items:
        cursor.execute("SELECT name, current_stock_usage FROM ingredients WHERE id = %s", (item['ingredient_id'],))
        ing = cursor.fetchone()
        if ing['current_stock_usage'] < item['amount_needed'] * jars_produced:
            db.close()
            return RedirectResponse(url=f"/production?error=Not enough {ing['name']}.", status_code=303)
    for item in recipe_items:
        cursor.execute("UPDATE ingredients SET current_stock_usage = current_stock_usage - %s WHERE id = %s", (item['amount_needed'] * jars_produced, item['ingredient_id']))
    cursor.execute("INSERT INTO production_batches (product_id, jars_produced, status) VALUES (%s, %s, 'in_progress')", (product_id, jars_produced))
    log_audit(request.session.get('username'), "PRODUCTION", f"Started batch of {jars_produced} jars.")
    db.commit()
    db.close()
    return RedirectResponse(url="/production?success=Batch started! Check Schedule.", status_code=303)

@app.get("/schedule", response_class=HTMLResponse, tags=["🏭 Production System"], summary="View Production Schedule & WIP")
async def schedule_page(request: Request, page_w: int = 1, page_c: int = 1, error: str = None, success: str = None):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    records_per_page = 10
    offset_w = (page_w - 1) * records_per_page
    offset_c = (page_c - 1) * records_per_page
    
    cursor.execute("SELECT COUNT(*) as total FROM production_batches WHERE status = 'in_progress'")
    total_pages_w = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    cursor.execute("SELECT pb.id, pb.created_at, p.name as product_name, pb.jars_produced, pb.status, pb.product_id FROM production_batches pb JOIN products p ON pb.product_id = p.id WHERE pb.status = 'in_progress' ORDER BY pb.created_at ASC LIMIT %s OFFSET %s", (records_per_page, offset_w))
    wip_data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM production_batches WHERE status = 'completed'")
    total_pages_c = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    cursor.execute("SELECT pb.id, pb.created_at, p.name as product_name, pb.jars_produced, pb.status, pb.product_id FROM production_batches pb JOIN products p ON pb.product_id = p.id WHERE pb.status = 'completed' ORDER BY pb.created_at DESC LIMIT %s OFFSET %s", (records_per_page, offset_c))
    completed_data = cursor.fetchall()
    
    db.close()
    return templates.TemplateResponse(request, "schedule.html", {
        "wip_batches": wip_data, "completed_batches": completed_data, "role": request.session.get('role'), 
        "error": error, "success": success, "current_page_w": page_w, "total_pages_w": total_pages_w,
        "current_page_c": page_c, "total_pages_c": total_pages_c, "per_page": records_per_page
    })

@app.post("/production/update", tags=["🏭 Production System"], summary="Mark Batch as Completed")
async def update_production_status(request: Request, batch_id: int = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM production_batches WHERE id = %s AND status = 'in_progress'", (batch_id,))
    batch = cursor.fetchone()
    if batch:
        cursor.execute("UPDATE products SET current_stock_jars = current_stock_jars + %s WHERE id = %s", (batch['jars_produced'], batch['product_id']))
        cursor.execute("UPDATE production_batches SET status = 'completed' WHERE id = %s", (batch_id,))
        log_audit(request.session.get('username'), "PRODUCTION", f"Batch #{batch_id} marked Completed.")
        db.commit()
    db.close()
    return RedirectResponse(url="/schedule?success=Batch marked Completed!", status_code=303)

# ==========================================
# INVENTORY ROUTES
# ==========================================

@app.get("/inventory", response_class=HTMLResponse, tags=["📦 Inventory Management"], summary="View Ingredient Stock & Restock History")
async def inventory_page(request: Request, page: int = 1):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ingredients LIMIT 9")
    ingredients_data = cursor.fetchall()
    
    records_per_page = 7
    offset = (page - 1) * records_per_page
    cursor.execute("SELECT COUNT(*) as total FROM ingredient_purchases")
    total_pages = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    
    cursor.execute("SELECT ip.id, ip.created_at, i.name as ingredient_name, ip.purchase_amount, i.purchase_unit, ip.cost FROM ingredient_purchases ip JOIN ingredients i ON ip.ingredient_id = i.id ORDER BY ip.created_at DESC LIMIT %s OFFSET %s", (records_per_page, offset))
    history_data = cursor.fetchall()
    db.close()
    return templates.TemplateResponse(request, "inventory.html", {"ingredients": ingredients_data, "history": history_data, "role": request.session.get('role'), "current_page": page, "total_pages": total_pages, "per_page": records_per_page})

@app.post("/inventory/purchase", tags=["📦 Inventory Management"], summary="Log Market Purchase")
async def log_purchase(request: Request, ingredient_id: int = Form(...), purchase_amount: float = Form(...), cost: float = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name, conversion_factor, purchase_unit, usage_unit FROM ingredients WHERE id = %s", (ingredient_id,))
    ingredient = cursor.fetchone()
    if ingredient:
        cursor.execute("UPDATE ingredients SET current_stock_usage = current_stock_usage + %s WHERE id = %s", (purchase_amount * float(ingredient['conversion_factor']), ingredient_id))
        cursor.execute("INSERT INTO ingredient_purchases (ingredient_id, purchase_amount, cost, restock_type) VALUES (%s, %s, %s, 'purchase')", (ingredient_id, purchase_amount, cost))
        log_audit(request.session.get('username'), "RESTOCK", f"Purchased {purchase_amount} {ingredient['purchase_unit']} of {ingredient['name']} for ₱{cost}.")
        db.commit()
    db.close()
    return RedirectResponse(url="/inventory", status_code=303)

@app.get("/harvest", response_class=HTMLResponse, tags=["📦 Inventory Management"], summary="View Herb Harvest Log")
async def harvest_page(request: Request, page: int = 1):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ingredients WHERE name IN ('Basil', 'Spinach', 'Malunggay', 'Mint')")
    herbs_data = cursor.fetchall()
    
    records_per_page = 9
    offset = (page - 1) * records_per_page
    cursor.execute("SELECT COUNT(*) as total FROM ingredient_purchases WHERE restock_type = 'harvest'")
    total_pages = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    
    cursor.execute("SELECT ip.id, ip.created_at, i.name as ingredient_name, ip.purchase_amount as harvest_amount, i.purchase_unit FROM ingredient_purchases ip JOIN ingredients i ON ip.ingredient_id = i.id WHERE ip.restock_type = 'harvest' ORDER BY ip.created_at DESC LIMIT %s OFFSET %s", (records_per_page, offset))
    harvest_history = cursor.fetchall()
    db.close()
    return templates.TemplateResponse(request, "harvest.html", {"herbs": herbs_data, "history": harvest_history, "role": request.session.get('role'), "current_page": page, "total_pages": total_pages, "per_page": records_per_page})

@app.post("/harvest", tags=["📦 Inventory Management"], summary="Log Farm Harvest")
async def log_harvest(request: Request, ingredient_id: int = Form(...), harvest_amount: float = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name, conversion_factor, purchase_unit FROM ingredients WHERE id = %s", (ingredient_id,))
    ingredient = cursor.fetchone()
    if ingredient:
        cursor.execute("UPDATE ingredients SET current_stock_usage = current_stock_usage + %s WHERE id = %s", (harvest_amount * float(ingredient['conversion_factor']), ingredient_id))
        cursor.execute("INSERT INTO ingredient_purchases (ingredient_id, purchase_amount, cost, restock_type) VALUES (%s, %s, 0.00, 'harvest')", (ingredient_id, harvest_amount))
        log_audit(request.session.get('username'), "HARVEST", f"Harvested {harvest_amount} {ingredient['purchase_unit']} of {ingredient['name']}.")
        db.commit()
    db.close()
    return RedirectResponse(url="/harvest", status_code=303)

# ==========================================
# CUSTOMERS ROUTE
# ==========================================

@app.get("/customers", response_class=HTMLResponse, tags=["👥 Customer Management"], summary="View Customer Profiles & Ledger")
async def customers_page(request: Request, page_l: int = 1, page_t: int = 1, search: str = None):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    records_per_page = 10
    offset_l = (page_l - 1) * records_per_page
    offset_t = (page_t - 1) * records_per_page
    
    cursor.execute("SELECT COUNT(DISTINCT customer_name) as total FROM orders")
    total_pages_l = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    cursor.execute("SELECT o.customer_name, COUNT(DISTINCT o.id) as total_orders, SUM(oi.quantity) as total_jars, SUM(oi.subtotal) as total_spent FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY o.customer_name ORDER BY total_spent DESC LIMIT %s OFFSET %s", (records_per_page, offset_l))
    customers_data = cursor.fetchall()
    
    count_query = "SELECT COUNT(*) as total FROM orders"
    if search:
        count_query += " WHERE customer_name LIKE %s"
        cursor.execute(count_query, (f"%{search}%",))
    else:
        cursor.execute(count_query)
        
    total_pages_t = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    
    order_query = "SELECT o.id, o.created_at, o.customer_name, o.total_price, o.payment_method, GROUP_CONCAT(CONCAT(oi.quantity, 'x ', p.name) SEPARATOR '<br>') as item_details FROM orders o JOIN order_items oi ON o.id = oi.order_id JOIN products p ON oi.product_id = p.id"
    if search: order_query += " WHERE o.customer_name LIKE %s"
    order_query += " GROUP BY o.id ORDER BY o.created_at DESC LIMIT %s OFFSET %s"
    
    if search: cursor.execute(order_query, (f"%{search}%", records_per_page, offset_t))
    else: cursor.execute(order_query, (records_per_page, offset_t))
    recent_orders = cursor.fetchall()
    
    db.close()
    return templates.TemplateResponse(request, "customers.html", {
        "customers": customers_data, "orders": recent_orders, 
        "current_page_l": page_l, "total_pages_l": total_pages_l,
        "current_page_t": page_t, "total_pages_t": total_pages_t,
        "per_page": records_per_page, "search_query": search or ""
    })

# ==========================================
# BUSINESS REPORTS ROUTES
# ==========================================

@app.get("/reports", response_class=HTMLResponse, tags=["📈 Business Analytics"], summary="View Sales & Analytics Reports")
async def reports_page(request: Request, page: int = 1, tab: str = 'charts'):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    records_per_page = 8
    offset = (page - 1) * records_per_page

    cursor.execute("SELECT COUNT(DISTINCT CONCAT(YEAR(created_at), WEEK(created_at))) as w_count FROM orders")
    w_total = cursor.fetchone()['w_count'] or 0
    cursor.execute("SELECT COUNT(DISTINCT CONCAT(YEAR(created_at), MONTH(created_at))) as m_count FROM orders")
    m_total = cursor.fetchone()['m_count'] or 0
    cursor.execute("SELECT COUNT(DISTINCT payment_method) as p_count FROM orders")
    p_total = cursor.fetchone()['p_count'] or 0
    
    total_pages = max(1, (max(w_total, m_total, p_total) + records_per_page - 1) // records_per_page)

    cursor.execute("SELECT CONCAT('Week ', WEEK(o.created_at)) AS period, COUNT(DISTINCT o.id) as total_orders, SUM(oi.quantity) as total_jars, SUM(oi.subtotal) as total_revenue FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY YEAR(o.created_at), WEEK(o.created_at) ORDER BY YEAR(o.created_at) DESC, WEEK(o.created_at) DESC LIMIT %s OFFSET %s", (records_per_page, offset))
    weekly_data = cursor.fetchall()
    
    cursor.execute("SELECT DATE_FORMAT(o.created_at, '%M %Y') AS period, COUNT(DISTINCT o.id) as total_orders, SUM(oi.quantity) as total_jars, SUM(oi.subtotal) as total_revenue FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY YEAR(o.created_at), MONTH(o.created_at) ORDER BY YEAR(o.created_at) DESC, MONTH(o.created_at) DESC LIMIT %s OFFSET %s", (records_per_page, offset))
    monthly_data = cursor.fetchall()
    
    cursor.execute("SELECT o.payment_method, COUNT(DISTINCT o.id) as total_orders, SUM(oi.subtotal) as total_revenue FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY o.payment_method ORDER BY total_revenue DESC LIMIT %s OFFSET %s", (records_per_page, offset))
    payment_data = cursor.fetchall()

    cursor.execute("SELECT CONCAT('Week ', WEEK(o.created_at)) AS period, SUM(oi.subtotal) as total_revenue FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY YEAR(o.created_at), WEEK(o.created_at) ORDER BY YEAR(o.created_at) DESC, WEEK(o.created_at) DESC LIMIT 10")
    weekly_chart = cursor.fetchall()

    cursor.execute("SELECT DATE_FORMAT(o.created_at, '%M %Y') AS period, SUM(oi.subtotal) as total_revenue FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY YEAR(o.created_at), MONTH(o.created_at) ORDER BY YEAR(o.created_at) DESC, MONTH(o.created_at) DESC LIMIT 10")
    monthly_chart = cursor.fetchall()

    cursor.execute("SELECT o.payment_method, SUM(oi.subtotal) as total_revenue FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY o.payment_method ORDER BY total_revenue DESC")
    payment_chart = cursor.fetchall()

    db.close()
    return templates.TemplateResponse(request, "reports.html", {
        "weekly": weekly_data, "monthly": monthly_data, "payments": payment_data,
        "weekly_chart": weekly_chart, "monthly_chart": monthly_chart, "payment_chart": payment_chart,
        "current_page": page, "total_pages": total_pages, "per_page": records_per_page,
        "active_tab": tab
    })

@app.get("/reports/print", response_class=HTMLResponse, tags=["📈 Business Analytics"], summary="Generate Printable PDF Summary")
async def print_report(request: Request):
    """Generates a beautifully formatted HTML page designed strictly for PDF Export."""
    if 'username' not in request.session or request.session.get('role') != 'admin':
        return RedirectResponse(url="/dashboard", status_code=303)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Overall Lifetime KPIs
    cursor.execute("SELECT COUNT(id) as total_orders, SUM(total_price) as total_revenue FROM orders WHERE status = 'completed'")
    kpis = cursor.fetchone()
    
    cursor.execute("SELECT SUM(quantity) as total_jars FROM order_items")
    jars = cursor.fetchone()
    kpis['total_jars'] = jars['total_jars'] if jars and jars['total_jars'] else 0
    
    # 2. Monthly Summary
    cursor.execute("""
        SELECT DATE_FORMAT(o.created_at, '%M %Y') AS period, COUNT(DISTINCT o.id) as total_orders, SUM(oi.quantity) as total_jars, SUM(oi.subtotal) as total_revenue
        FROM orders o JOIN order_items oi ON o.id = oi.order_id
        WHERE o.status = 'completed'
        GROUP BY YEAR(o.created_at), MONTH(o.created_at) ORDER BY YEAR(o.created_at) DESC, MONTH(o.created_at) DESC
    """)
    monthly_data = cursor.fetchall()
    
    # 3. Weekly Summary
    cursor.execute("""
        SELECT CONCAT('Week ', WEEK(o.created_at), ', ', YEAR(o.created_at)) AS period, COUNT(DISTINCT o.id) as total_orders, SUM(oi.quantity) as total_jars, SUM(oi.subtotal) as total_revenue
        FROM orders o JOIN order_items oi ON o.id = oi.order_id
        WHERE o.status = 'completed'
        GROUP BY YEAR(o.created_at), WEEK(o.created_at) ORDER BY YEAR(o.created_at) DESC, WEEK(o.created_at) DESC LIMIT 15
    """)
    weekly_data = cursor.fetchall()

    # 4. Top Products All-Time
    cursor.execute("""
        SELECT p.name, SUM(oi.quantity) as total_sold, SUM(oi.subtotal) as total_revenue
        FROM order_items oi JOIN products p ON oi.product_id = p.id
        GROUP BY p.id ORDER BY total_sold DESC
    """)
    product_data = cursor.fetchall()

    db.close()
    
    from datetime import datetime
    current_date = datetime.now().strftime("%B %d, %Y")
    admin_name = request.session.get('username')
    
    return templates.TemplateResponse(request, "report_print.html", {
        "kpis": kpis,
        "monthly": monthly_data,
        "weekly": weekly_data,
        "products": product_data,
        "date": current_date,
        "generated_by": admin_name
    })

# ==========================================
# USER & SETTINGS ROUTES 
# ==========================================

@app.get("/settings", response_class=HTMLResponse, tags=["⚙️ User Administration"], summary="View Account Settings")
async def settings_page(request: Request, error: str = None, success: str = None):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, full_name, role FROM users WHERE id = %s", (request.session.get('user_id'),))
    user_data = cursor.fetchone()
    db.close()
    
    return templates.TemplateResponse(request, "settings.html", {"user": user_data, "error": error, "success": success})

@app.post("/settings/update", tags=["⚙️ User Administration"], summary="Update Personal Profile & Password")
async def update_settings(request: Request, username: str = Form(...), full_name: str = Form(...), old_password: str = Form(""), new_password: str = Form(""), confirm_password: str = Form("")):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    
    user_id = request.session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT id FROM users WHERE username = %s AND id != %s", (username, user_id))
    if cursor.fetchone():
        db.close()
        return RedirectResponse(url="/settings?error=That username is already taken.", status_code=303)
        
    if old_password or new_password or confirm_password:
        if not old_password or not new_password or not confirm_password:
            db.close()
            return RedirectResponse(url="/settings?error=Please fill out all 3 password fields to change your password.", status_code=303)
        if new_password != confirm_password:
            db.close()
            return RedirectResponse(url="/settings?error=New passwords do not match.", status_code=303)
            
        cursor.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
        current_user = cursor.fetchone()
        if current_user['password_hash'] != old_password:
            db.close()
            return RedirectResponse(url="/settings?error=Incorrect old password.", status_code=303)
            
        cursor.execute("UPDATE users SET username = %s, full_name = %s, password_hash = %s WHERE id = %s", (username, full_name, new_password, user_id))
    else:
        cursor.execute("UPDATE users SET username = %s, full_name = %s WHERE id = %s", (username, full_name, user_id))
        
    request.session['username'] = username
    log_audit(username, "SYSTEM", f"User {username} updated their profile settings.")
    db.commit()
    db.close()
    return RedirectResponse(url="/settings?success=Profile updated successfully!", status_code=303)

@app.get("/users", response_class=HTMLResponse, tags=["⚙️ User Administration"], summary="Manage Team Roles & Accounts")
async def users_page(request: Request, error: str = None, success: str = None):
    if request.session.get('role') != 'admin': return RedirectResponse(url="/dashboard", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, full_name, role, created_at FROM users WHERE status = 'active'")
    users_data = cursor.fetchall()
    db.close()
    return templates.TemplateResponse(request, "users.html", {"request": request, "users": users_data, "user_count": len(users_data), "current_user": request.session.get('username'), "error": error, "success": success, "per_page": 4})

@app.post("/users", tags=["⚙️ User Administration"], summary="Create New User Account")
async def create_user(request: Request, username: str = Form(...), full_name: str = Form(...), role: str = Form(...), password: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT full_name FROM users WHERE role = %s AND status = 'active'", (role,))
    if cursor.fetchone(): db.close(); return RedirectResponse(url=f"/users?error=Role active.", status_code=303)
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE status = 'active'")
    if cursor.fetchone()['count'] < 4:
        cursor.execute("INSERT INTO users (username, full_name, role, password_hash, status) VALUES (%s, %s, %s, %s, 'active')", (username, full_name, role, password))
        log_audit(request.session.get('username'), "SYSTEM", f"Created {role} account.")
        db.commit()
        db.close()
        return RedirectResponse(url="/users?success=Added user.", status_code=303)
    db.close()
    return RedirectResponse(url="/users?error=Limit reached.", status_code=303)

@app.post("/users/delete", tags=["⚙️ User Administration"], summary="Deactivate User Account")
async def remove_user(request: Request, user_id: int = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("UPDATE users SET status = 'inactive' WHERE id = %s", (user_id,))
    db.commit()
    db.close()
    return RedirectResponse(url="/users?success=User deactivated.", status_code=303)

# ==========================================
# SYSTEM AUDIT ROUTE
# ==========================================

@app.get("/audit", response_class=HTMLResponse, tags=["📋 System Logs"], summary="View Audit Log & Access History")
async def audit_page(request: Request, page_a: int = 1, page_l: int = 1):
    if 'username' not in request.session: return RedirectResponse(url="/", status_code=303)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    records_per_page = 10
    offset_a = (page_a - 1) * records_per_page
    offset_l = (page_l - 1) * records_per_page
    
    cursor.execute("SELECT COUNT(*) as total FROM audit_log")
    total_pages_a = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    cursor.execute("SELECT * FROM audit_log ORDER BY created_at DESC LIMIT %s OFFSET %s", (records_per_page, offset_a))
    logs_data = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) as total FROM login_history")
    total_pages_l = max(1, (cursor.fetchone()['total'] + records_per_page - 1) // records_per_page)
    cursor.execute("SELECT * FROM login_history ORDER BY created_at DESC LIMIT %s OFFSET %s", (records_per_page, offset_l))
    logins_data = cursor.fetchall()
    
    db.close()
    return templates.TemplateResponse(request, "audit.html", {
        "logs": logs_data, "logins": logins_data, 
        "current_page_a": page_a, "total_pages_a": total_pages_a,
        "current_page_l": page_l, "total_pages_l": total_pages_l,
        "per_page": records_per_page
    })