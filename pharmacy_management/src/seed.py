import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services import user_service

def seed_database():
    """Seeds the database with initial roles and permissions."""

    # Create roles
    admin_role_id = user_service.create_role("admin")
    pharmacist_role_id = user_service.create_role("pharmacist")

    # Create permissions
    permissions = [
        "manage_inventory",
        "view_inventory",
        "manage_sales",
        "view_sales",
        "manage_patients",
        "view_patients",
        "manage_suppliers",
        "view_suppliers",
        "manage_prescriptions",
        "view_prescriptions",
        "view_reports",
        "manage_users"
    ]

    permission_ids = {name: user_service.create_permission(name) for name in permissions}

    # Assign all permissions to admin
    if admin_role_id is not None:
        for perm_id in permission_ids.values():
            if perm_id is not None:
                user_service.assign_permission_to_role(admin_role_id, perm_id)

    # Assign permissions to pharmacist
    if pharmacist_role_id is not None:
        pharmacist_perms = [
            "manage_inventory", "view_inventory", "manage_sales", "view_sales",
            "manage_patients", "view_patients", "view_suppliers", "manage_prescriptions",
            "view_prescriptions"
        ]
        for perm_name in pharmacist_perms:
            perm_id = permission_ids.get(perm_name)
            if perm_id is not None:
                user_service.assign_permission_to_role(pharmacist_role_id, perm_id)

    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()
