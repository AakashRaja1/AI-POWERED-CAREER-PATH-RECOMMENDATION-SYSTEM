"""
Script to add is_admin column to existing User table.
Run this if you get an error about is_admin column not existing.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import text
from app.database.session import engine

def add_admin_column():
    """Add is_admin column to User table if it doesn't exist"""
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='user' AND column_name='is_admin'
            """))
            exists = result.fetchone()
            
            if not exists:
                # Add the column
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"))
                conn.commit()
                print("✓ Added is_admin column to User table")
            else:
                print("✓ is_admin column already exists")
    except Exception as e:
        print(f"Error: {e}")
        print("\nYou may need to manually add the column:")
        print("ALTER TABLE \"user\" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;")

if __name__ == "__main__":
    add_admin_column()



