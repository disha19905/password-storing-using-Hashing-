import bcrypt
import mysql.connector

# === CONFIGURATION ===
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # or another MySQL user
    'password': 'root',  # change it
    'database': 'my_app_db'
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def register_user(username: str, password: str) -> bool:
    """Register a new user with hashed password."""
    pw_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed.decode('utf-8'))
        )
        conn.commit()
    except mysql.connector.Error as err:
        print("Error during registration:", err)
        cursor.close()
        conn.close()
        return False
    cursor.close()
    conn.close()
    return True


def login_user(username: str, password: str) -> bool:
    """Verify credentials and return True if login succeeds."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_hash FROM users WHERE username = %s",
        (username,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        return False

    stored_hash = row[0].encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)


def main():
    current_user = None

    while True:
        print("\n=== MENU ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            uname = input("Choose username: ").strip()
            pwd = input("Choose password: ").strip()
            success = register_user(uname, pwd)
            if success:
                print("[+] Registration successful.")
            else:
                print("[!] Registration failed (maybe username exists).")

        elif choice == '2':
            uname = input("Username: ").strip()
            pwd = input("Password: ").strip()
            if login_user(uname, pwd):
                print("[+] Login successful. Welcome,", uname)
                current_user = uname
                # After login — you can show a “logged‑in” menu or break
                break
            else:
                print("[!] Login failed. Invalid credentials.")

        elif choice == '3':
            print("Goodbye.")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
