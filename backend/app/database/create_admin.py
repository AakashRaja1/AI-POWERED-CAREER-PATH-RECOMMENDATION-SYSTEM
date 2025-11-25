"""
Script to create admin user in the database.
Run this once to create the admin account.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.session import engine, get_session
from app.database.models import User
from app.database import crud
from app.core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    """Create admin user if it doesn't exist"""
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD
    
    with next(get_session()) as session:
        # Check if admin already exists
        existing_admin = crud.get_user_by_email(session, email=admin_email)
        if existing_admin:
            if existing_admin.is_admin:
                print(f"✓ Admin user already exists: {admin_email}")
                return
            else:
                # Update existing user to admin
                existing_admin.is_admin = True
                session.add(existing_admin)
                session.commit()
                print(f"✓ Updated user to admin: {admin_email}")
                return
        
        # Create new admin user
        hashed_password = pwd_context.hash(admin_password)
        admin_user = User(
            full_name="Admin User",
            email=admin_email,
            password=hashed_password,
            is_admin=True
        )
        crud.create_user(session, admin_user)
        print(f"✓ Admin user created successfully!")
        print(f"  Email: {admin_email}")
        print(f"  Password: {admin_password}")
        print("\n⚠️  IMPORTANT: Change the admin password in production!")

if __name__ == "__main__":
    create_admin()



