import sys
import os
from getpass import getpass

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import logging
from src.utils.logging_config import setup_logging
from src.utils.permissions import requires_permission
from src.services import user_service, inventory_service, sales_service, patient_service, supplier_service, reporting_service, prescription_service
from src.models.sale import SaleItem
from datetime import date

@requires_permission("manage_inventory")
def inventory_menu(current_user):
    """Displays the inventory management menu and handles user choices."""
    while True:
        print("\nInventory Management:")
        print("1. Add Medicine")
        print("2. View All Medicines")
        print("3. Search for a Medicine")
        # ... (other options)
        print("8. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            # ... (implementation)
        elif choice == '2':
            page = 1
            page_size = 5
            while True:
                total_medicines = inventory_service.get_total_medicines_count()
                total_pages = (total_medicines + page_size - 1) // page_size

                medicines = inventory_service.get_all_medicines(page, page_size)

                print(f"\n--- Medicines (Page {page}/{total_pages}) ---")
                if medicines:
                    for med in medicines:
                        print(f"ID: {med.id}, Name: {med.name}, Manufacturer: {med.manufacturer}, Price: {med.price}, Qty: {med.quantity}, Expiry: {med.expiry_date}")
                else:
                    print("No medicines found.")

                print("\nEnter 'n' for next page, 'p' for previous, or 'b' to go back.")
                nav = input("> ")
                if nav == 'n':
                    if page < total_pages:
                        page += 1
                    else:
                        print("Already on the last page.")
                elif nav == 'p':
                    if page > 1:
                        page -= 1
                    else:
                        print("Already on the first page.")
                elif nav == 'b':
                    break
        elif choice == '3':
            term = input("Enter search term (name or manufacturer): ")
            medicines = inventory_service.search_medicines(term)
            if medicines:
                for med in medicines:
                    print(f"ID: {med.id}, Name: {med.name}, Manufacturer: {med.manufacturer}, Price: {med.price}, Quantity: {med.quantity}, Expiry: {med.expiry_date}")
            else:
                print("No medicines found matching your search.")
        elif choice == '8':
            break
        else:
            print("Invalid choice. To be implemented.")

@requires_permission("manage_sales")
def sales_menu(current_user):
    """Displays the sales management menu and handles user choices."""
    # ... (implementation remains the same)

@requires_permission("manage_patients")
def patient_menu(current_user):
    """Displays the patient management menu and handles user choices."""
    # ... (implementation remains the same)

@requires_permission("manage_suppliers")
def supplier_menu(current_user):
    """Displays the supplier management menu and handles user choices."""
    # ... (implementation remains the same)

@requires_permission("view_reports")
def reporting_menu(current_user):
    """Displays the reporting menu and handles user choices."""
    # ... (implementation remains the same)

@requires_permission("manage_prescriptions")
def prescription_menu(current_user):
    """Displays the prescription management menu and handles user choices."""
    # ... (implementation remains the same)

@requires_permission("manage_users")
def user_management_menu(current_user):
    """Displays the user management menu and handles user choices."""
    while True:
        print("\nUser Management:")
        print("1. Create New User")
        print("2. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter new username: ")
            password = getpass("Enter new password: ")

            # Display roles to choose from
            roles = user_service.get_all_roles() # I need to implement this function
            if not roles:
                print("No roles found. Please create roles first.")
                continue

            print("\nPlease select a role:")
            for role in roles:
                print(f"ID: {role['id']}, Name: {role['name']}")
            role_id = int(input("Enter role ID: "))

            user_service.create_user(username, password, role_id)
            print("User created successfully.")
        elif choice == '2':
            break
        else:
            print("Invalid choice.")

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
        print("4. Supplier Management")
        print("5. Prescription Management")
        print("6. Reporting")
        print("7. User Management")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            inventory_menu(current_user)
        elif choice == '2':
            sales_menu(current_user)
        elif choice == '3':
            patient_menu(current_user)
        elif choice == '4':
            supplier_menu(current_user)
        elif choice == '5':
            prescription_menu(current_user)
        elif choice == '6':
            reporting_menu(current_user)
        elif choice == '7':
            user_management_menu(current_user)
        elif choice == '8':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
