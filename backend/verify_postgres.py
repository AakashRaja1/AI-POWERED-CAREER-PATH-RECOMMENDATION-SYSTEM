#!/usr/bin/env python3
"""Verify PostgreSQL database connection and content"""
import sys
sys.path.insert(0, '.')
from sqlmodel import Session, select
from app.database.session import engine
from app.database.models import User

try:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print(f"✓ PostgreSQL Connection Successful!")
        print(f"✓ Database: career_recommendations")
        print(f"✓ Total users in database: {len(users)}")
        for user in users:
            print(f"  - {user.email} (Admin: {user.is_admin})")
except Exception as e:
    print(f"✗ Database Connection Failed: {e}")
    import traceback
    traceback.print_exc()
