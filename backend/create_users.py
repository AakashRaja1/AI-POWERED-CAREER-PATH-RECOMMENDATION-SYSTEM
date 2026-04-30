#!/usr/bin/env python3
"""Create default users for testing"""
import sys
sys.path.insert(0, '.')
from sqlmodel import Session
from app.database.session import engine
from app.database.models import User
from passlib.context import CryptContext

# Use argon2 which has better Windows support than bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

with Session(engine) as session:
    # Create or update admin
    admin = session.query(User).filter(User.email == "admin@careerpath.com").first()
    if admin:
        print(f"✓ Admin user exists. Updating password...")
        admin.password = pwd_context.hash("admin123")
    else:
        admin = User(
            full_name="Admin User",
            email="admin@careerpath.com",
            password=pwd_context.hash("admin123"),
            is_admin=True
        )
        print(f"✓ Creating admin user...")
    
    session.add(admin)
    session.commit()
    print(f"✓ Admin user ready: admin@careerpath.com / admin123")

    # Create test user
    test = session.query(User).filter(User.email == "test@test.com").first()
    if not test:
        test = User(
            full_name="Test User",
            email="test@test.com",
            password=pwd_context.hash("password123"),
            is_admin=False
        )
        session.add(test)
        session.commit()
        print(f"✓ Test user created: test@test.com / password123")
    else:
        print(f"✓ Test user already exists")
