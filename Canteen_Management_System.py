import mysql.connector

# Database Connection
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  
        password='Rishi#2004',  
        database='canteen_db'
    )

# Function to register a new user
def register_user():
    conn = get_connection()
    cursor = conn.cursor()
    print("\n--- Register New User ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match!")
        conn.close()
        return

    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    role = 'customer'  

    try:
        cursor.execute("INSERT INTO users (username, password, email, phone, role) VALUES (%s, %s, %s, %s, %s)",
                       (username, password, email, phone, role))
        conn.commit()
        print("Registration successful!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


# Function to login a user
def login_user():
    conn = get_connection()
    cursor = conn.cursor()
    print("\n--- User Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT user_id, role FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"Logged in as {result[1]}")
        return result
    else:
        print("Invalid credentials!")
        return None


# Function to view menu
def view_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu WHERE availability=1")
    items = cursor.fetchall()
    print("\n--- Menu ---")
    for item in items:
        print(f"{item[0]}. {item[1]} - ${item[2]}")
    conn.close()


# Function to place an order
def place_order(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    view_menu()
    item_id = int(input("Enter the item ID to order: "))
    quantity = int(input("Enter quantity: "))

    cursor.execute("INSERT INTO orders (user_id, item_id, quantity) VALUES (%s, %s, %s)", (user_id, item_id, quantity))
    conn.commit()
    print("Order placed successfully!")
    conn.close()


# Function to provide feedback
def give_feedback(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    item_id = int(input("Enter the item ID to review: "))
    rating = int(input("Rate the item (1-5): "))
    comments = input("Enter your feedback: ")

    cursor.execute("INSERT INTO feedback (user_id, item_id, rating, comments) VALUES (%s, %s, %s, %s)",
                   (user_id, item_id, rating, comments))
    conn.commit()
    print("Feedback submitted!")
    conn.close()


# Admin: Add menu item
def add_menu_item():
    conn = get_connection()
    cursor = conn.cursor()
    item_name = input("Enter item name: ")
    price = float(input("Enter item price: "))

    cursor.execute("INSERT INTO menu (item_name, price) VALUES (%s, %s)", (item_name, price))
    conn.commit()
    print("Item added successfully!")
    conn.close()


# Admin: Update menu item
def update_menu_item():
    conn = get_connection()
    cursor = conn.cursor()
    item_id = int(input("Enter item ID to update: "))
    new_price = float(input("Enter new price: "))

    cursor.execute("UPDATE menu SET price=%s WHERE item_id=%s", (new_price, item_id))
    conn.commit()
    print("Item updated successfully!")
    conn.close()


# Main function with menu-driven interface
def main():
    print("Welcome to the Smart Canteen Management System!")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            register_user()
        elif choice == 2:
            user = login_user()
            if user:
                user_id, role = user
                if role == 'customer':
                    while True:
                        print("\n1. View Menu\n2. Place Order\n3. Give Feedback\n4. Logout")
                        action = int(input("Choose an action: "))
                        if action == 1:
                            view_menu()
                        elif action == 2:
                            place_order(user_id)
                        elif action == 3:
                            give_feedback(user_id)
                        elif action == 4:
                            break
                elif role == 'admin':
                    while True:
                        print("\n1. Add Menu Item\n2. Update Menu Item\n3. Logout")
                        action = int(input("Choose an action: "))
                        if action == 1:
                            add_menu_item()
                        elif action == 2:
                            update_menu_item()
                        elif action == 3:
                            break
        elif choice == 3:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()

