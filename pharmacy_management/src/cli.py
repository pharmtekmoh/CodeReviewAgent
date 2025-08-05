import sys
import os
from getpass import getpass

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import logging
from src.utils.logging_config import setup_logging
from src.services import user_service, inventory_service, sales_service, patient_service
from src.models.sale import SaleItem
from datetime import date

def inventory_menu():
    """Displays the inventory management menu and handles user choices."""
    while True:
        print("\nInventory Management:")
        print("1. Add Medicine")
        print("2. View All Medicines")
        # ... (other options)
        print("8. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            # ... (implementation)
        elif choice == '2':
            # ... (implementation)
        elif choice == '8':
            break
        else:
            print("Invalid choice. To be implemented.")

def sales_menu(current_user):
    """Displays the sales management menu and handles user choices."""
    while True:
        print("\nSales Management:")
        print("1. Create New Sale")
        print("2. View All Sales")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            items = []
            while True:
                med_id = input("Enter medicine ID (or 'done' to finish): ")
                if med_id.lower() == 'done':
                    break
                quantity = int(input("Enter quantity: "))
                items.append(SaleItem(medicine_id=int(med_id), quantity=quantity))

            if items:
                sales_service.create_sale(current_user.id, items)
                print("Sale created successfully.")
        elif choice == '2':
            sales = sales_service.get_all_sales()
            if sales:
                for sale in sales:
                    print(f"Sale ID: {sale.id}, Timestamp: {sale.timestamp}, User ID: {sale.user_id}")
                    for item in sale.items:
                        print(f"  - Medicine ID: {item.medicine_id}, Quantity: {item.quantity}")
            else:
                print("No sales found.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. To be implemented.")

def patient_menu():
    """Displays the patient management menu and handles user choices."""
    while True:
        print("\nPatient Management:")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter patient name: ")
            address = input("Enter address: ")
            phone = input("Enter phone number: ")
            patient_service.add_patient(name, address, phone)
            print("Patient added successfully.")
        elif choice == '2':
            patients = patient_service.get_all_patients()
            if patients:
                for p in patients:
                    print(f"ID: {p.id}, Name: {p.name}, Address: {p.address}, Phone: {p.phone}")
            else:
                print("No patients found.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. To be implemented.")

def main():
    """The main function of the command-line interface."""
    setup_logging()
    logging.info("Application started.")

    print("Welcome to the Pharmacy Management System!")

    current_user = None
    while not current_user:
        username = input("Username: ")
        password = getpass("Password: ")
        try:
            if not user_service.get_user_by_username("admin"):
                user_service.create_user("admin", "admin", "admin")
            current_user = user_service.check_user(username, password)
            if not current_user:
                logging.warning(f"Failed login attempt for username: {username}")
                print("Invalid username or password. Please try again.")
        except Exception as e:
            logging.error(f"An error occurred during login: {e}")
            print("An error occurred. Please try again later.")

    logging.info(f"User '{current_user.username}' logged in successfully.")
    print(f"\nWelcome, {current_user.username}! Your role is: {current_user.role}")

    while True:
        print("\nMain Menu:")
        print("1. Inventory Management")
        print("2. Sales Management")
        print("3. Patient Management")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            inventory_menu()
        elif choice == '2':
            sales_menu(current_user)
        elif choice == '3':
            patient_menu()
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
