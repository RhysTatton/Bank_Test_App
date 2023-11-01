import sqlite3
import hashlib
import requests


def user_login():
    db = sqlite3.connect('basic_bank.db')
    cursor = db.cursor()
    user_id = None
    try:
        username = input("\nUsername: ")
        password = input("\nPassword: ")

        cursor.execute('''SELECT id, password_hash FROM users WHERE username = ?''', (username,))
        user = cursor.fetchone()

        if user:
            user_id, stored_password_hash = user
            input_password_hash = hashlib.sha256(password.encode()).hexdigest()

            if stored_password_hash == input_password_hash:
                return user_id
            else:
                print("\nIncorrect Password")
        else:
            print("\nUsername not found")
        db.close()
    except sqlite3.Error as e:
        print("\nDatabase error:", str(e))
    except Exception as e:
        print("\nAn error occurred:", str(e))

    return user_id


def register_user():
    db = sqlite3.connect('basic_bank.db')
    cursor = db.cursor()
    try:
        reg_username = input("\nPlease enter a username: ")
        reg_password = input("\nPlease enter a password: ")
        reg_balance = float(input("\nPlease enter how much you wish to put into the account on start up: "))

        password_hash = hashlib.sha256(reg_password.encode()).hexdigest()

        user = [reg_username, password_hash, reg_balance]

        cursor.execute(''' INSERT INTO users(username, password_hash, balance) VALUES(?,?,?)''', user)
        db.commit()
    except (ValueError, Exception) as e:
        print("\n Error adding user", e)
        db.rollback()
    db.close()


def second_menu(user_id):
    while True:
        try:
            second_menu_choice = int(input(f'''\nWelcome, User: {user_id} 
    
            Please enter the number for what you wish to do: 
                                
            1. Transfer Funds
            2. Add Funds
            3. Check Balance
            4. Quit
                                
            > '''))

            if second_menu_choice == 1:
                sender_id = user_id
                receiver_id = int(input("\nEnter the ID of the account you wish to send to: "))
                amount = float(input("\nEnter the amount you wish to send: "))
                transfer(sender_id, receiver_id, amount)

            elif second_menu_choice == 2:
                add_funds(user_id)

            elif second_menu_choice == 3:
                check_balance(user_id)

            elif second_menu_choice == 4:
                print("\n You have successfully logged out. Thank you for using our App")
                break

            else:
                print("\nYou have entered an invalid amount")

        except ValueError as e:
            print("\nYou have entered an invalid amount", e)


def transfer(sender_id, receiver_id, amount):
    try:
        transfer_data = {
            "Sender-id": sender_id,
            "receiver_id": receiver_id,
            "amount": amount
        }

        api_url = 'Place Holder API'

        api_response = requests.post(api_url, json=transfer_data)

        if api_response.status_code == 200:
            print("\nTransfer Successful")
            try:
                db = sqlite3.connect('basic_bank.db')
                cursor = db.cursor()

                cursor.execute('''SELECT balance FROM users WHERE id = ?''', (sender_id,))
                sender_balance = cursor.fetchone()[0]

                if sender_balance < amount:
                    db.close()
                    print("You do not have enough in your balance for this transaction")
                    return False

                cursor.execute('''UPDATE users SET balance = balance - ? WHERE id = ?''',
                               (amount, sender_id))

                cursor.execute('''UPDATE users SET balance = balance + ? WHERE id = ?''',
                               (amount, receiver_id))

                cursor.execute('''INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (?,?,?)''',
                               (sender_id, receiver_id, amount))

                db.commit()
                db.close()
                return True
            except sqlite3.Error as e:
                print("\nDatabase error:", str(e))
            return True
        else:
            print("\nTransfer has failed: ", api_response.text)
            return False
    except requests.exceptions.RequestException as e:
        print("Request error:", str(e))
        return False


def add_funds(user_id):
    try:
        db = sqlite3.connect('basic_bank.db')
        cursor = db.cursor()

        funds_amount = float(input("\nHow much would you like to add to the account? "))

        cursor.execute('''UPDATE users SET balance = balance + ? WHERE id = ?''',
                       (funds_amount, user_id))

        print("\n Funds have successfully been added")
        db.commit()
        db.close()

    except sqlite3.Error as e:
        print("\nDatabase error:", str(e))


def check_balance(user_id):
    try:
        db = sqlite3.connect('basic_bank.db')
        cursor = db.cursor()

        cursor.execute('''SELECT balance FROM users WHERE id = ?''', (user_id,))
        user_balance = cursor.fetchone()

        print("\nYour Balance is: ", user_balance)

        db.commit()
        db.close()

    except sqlite3.Error as e:
        print("\nDatabase error:", str(e))


try:
    initial_menu = int(input('''\nWelcome to the BankTest App!
    
    Please enter the number for what you wish to do: 
                                
    1. Login
    2. Register
    3. Quit
                                
    > '''))

    if initial_menu == 1:
        user_id = user_login()
        if user_id is not None:
            second_menu(user_id)

    elif initial_menu == 2:
        register_user()

    elif initial_menu == 3:
        print("\nThank you for using the BankTest App")

    else:
        print("\nYou have entered an invalid input")

except ValueError as e:
    print("\nYou have entered an invalid input")
