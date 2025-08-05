import sys
import os
from getpass import getpass

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import logging
from src.utils.logging_config import setup_logging
from src.services import user_service, inventory_service, sales_service, patient_service, supplier_service, reporting_service, prescription_service
from src.models.sale import SaleItem
from datetime import date

def inventory_menu():
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
            page = 1
            page_size = 5
            while True:
                total_patients = patient_service.get_total_patients_count()
                total_pages = (total_patients + page_size - 1) // page_size

                patients = patient_service.get_all_patients(page, page_size)

                print(f"\n--- Patients (Page {page}/{total_pages}) ---")
                if patients:
                    for p in patients:
                        print(f"ID: {p.id}, Name: {p.name}, Address: {p.address}, Phone: {p.phone}")
                else:
                    print("No patients found.")

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
            break
        else:
            print("Invalid choice. To be implemented.")

def supplier_menu():
    """Displays the supplier management menu and handles user choices."""
    while True:
        print("\nSupplier Management:")
        print("1. Add Supplier")
        print("2. View All Suppliers")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter supplier name: ")
            contact = input("Enter contact person: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")
            supplier_service.add_supplier(name, contact, phone, address)
            print("Supplier added successfully.")
        elif choice == '2':
            page = 1
            page_size = 5
            while True:
                total_suppliers = supplier_service.get_total_suppliers_count()
                total_pages = (total_suppliers + page_size - 1) // page_size

                suppliers = supplier_service.get_all_suppliers(page, page_size)

                print(f"\n--- Suppliers (Page {page}/{total_pages}) ---")
                if suppliers:
                    for s in suppliers:
                        print(f"ID: {s.id}, Name: {s.name}, Contact: {s.contact_person}, Phone: {s.phone}, Address: {s.address}")
                else:
                    print("No suppliers found.")

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
        elif choice == '5':
            break
        else:
            print("Invalid choice. To be implemented.")

def reporting_menu():
    """Displays the reporting menu and handles user choices."""
    while True:
        print("\nReporting:")
        print("1. Sales Report by User")
        print("2. Sales Report by Date Range")
        print("3. Inventory Value Report")
        print("4. Expiring Medicines Report")
        print("5. Export Sales to CSV")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            # ... (implementation)
        elif choice == '2':
            # ... (implementation)
        elif choice == '3':
            # ... (implementation)
        elif choice == '4':
            # ... (implementation)
        elif choice == '5':
            print("\nExport Sales Report to CSV:")
            print("1. All Sales")
            print("2. Sales by Date Range")
            export_choice = input("Choose a report to export: ")

            sales_to_export = []
            if export_choice == '1':
                sales_to_export = sales_service.get_all_sales()
            elif export_choice == '2':
                start_date_str = input("Enter start date (YYYY-MM-DD): ")
                end_date_str = input("Enter end date (YYYY-MM-DD): ")
                start_date = date.fromisoformat(start_date_str)
                end_date = date.fromisoformat(end_date_str)
                sales_to_export = reporting_service.get_sales_by_date_range(start_date, end_date)

            if sales_to_export:
                filename = f"sales_report_{date.today()}.csv"
                if reporting_service.export_sales_to_csv(sales_to_export, filename):
                    print(f"Report exported to {filename}")
                else:
                    print("Failed to export report.")
            else:
                print("No sales data to export.")
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

def prescription_menu():
    """Displays the prescription management menu and handles user choices."""
    while True:
        print("\nPrescription Management:")
        print("1. Create New Prescription")
        print("2. View Prescriptions by Patient")
        print("3. Fill Prescription")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            patient_id = int(input("Enter patient ID: "))
            doctor = input("Enter doctor's name: ")
            med_id = int(input("Enter medicine ID: "))
            qty = int(input("Enter quantity: "))
            pres_date = date.today()
            prescription_service.create_prescription(patient_id, doctor, med_id, qty, pres_date)
            print("Prescription created successfully.")
        elif choice == '2':
            patient_id = int(input("Enter patient ID: "))
            prescriptions = prescription_service.get_prescriptions_by_patient(patient_id)
            if prescriptions:
                for p in prescriptions:
                    print(f"ID: {p.id}, Dr: {p.doctor_name}, Med ID: {p.medicine_id}, Qty: {p.quantity}, Date: {p.prescription_date}, Filled: {p.filled}")
            else:
                print("No prescriptions found for this patient.")
        elif choice == '3':
            pres_id = int(input("Enter prescription ID to fill: "))
            if prescription_service.fill_prescription(pres_id):
                print("Prescription filled successfully.")
            else:
                print("Failed to fill prescription. Check logs for details.")
        elif choice == '4':
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
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            inventory_menu()
        elif choice == '2':
            sales_menu(current_user)
        elif choice == '3':
            patient_menu()
        elif choice == '4':
            supplier_menu()
        elif choice == '5':
            prescription_menu()
        elif choice == '6':
            reporting_menu()
        elif choice == '7':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
