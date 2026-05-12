from database import get_db_connection
import bcrypt

def reset_passwords():
    # 1. Connect to your database
    db = get_db_connection()
    if not db:
        print("Could not connect to the database.")
        return
        
    cursor = db.cursor()

    # 2. Generate mathematically valid bcrypt hashes
    print("Generating secure hashes...")
    admin_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    maria_hash = bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 3. Update the database
    print("Updating database...")
    cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'admin'", (admin_hash,))
    cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'Maria'", (maria_hash,))

    db.commit()
    db.close()
    
    print("✅ Success! Passwords have been securely updated. You can now log in.")

if __name__ == "__main__":
    reset_passwords()