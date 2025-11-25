"""
Database setup script to create the database if it doesn't exist.
Run this script before starting the FastAPI server.
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from app.core.config import settings
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)

def create_database():
    """Create the database if it doesn't exist"""
    # Parse the database URL
    db_url = settings.DATABASE_URL
    
    # Handle different URL formats
    if not db_url.startswith("postgresql://"):
        print("Error: DATABASE_URL must start with 'postgresql://'")
        return False
    
    # Remove the protocol
    url_without_protocol = db_url.replace("postgresql://", "")
    
    # Split by @ to separate credentials from host/database
    if "@" not in url_without_protocol:
        print("Error: Invalid DATABASE_URL format (missing @)")
        return False
    
    # Split into credentials and host/database
    creds_part, host_db_part = url_without_protocol.split("@", 1)
    
    # Extract database name (last part after /)
    if "/" not in host_db_part:
        print("Error: Invalid DATABASE_URL format (missing database name)")
        return False
    
    db_name = host_db_part.split("/")[-1]
    
    # Build connection string to postgres database
    conn_string = f"postgresql://{creds_part}@{host_db_part.rsplit('/', 1)[0]}/postgres"
    
    try:
        # Connect to PostgreSQL server (to default 'postgres' database)
        conn = psycopg2.connect(conn_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✓ Database '{db_name}' created successfully")
        else:
            print(f"✓ Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ Error connecting to PostgreSQL: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Connection credentials are correct")
        print("3. The 'postgres' database is accessible")
        print(f"\nAttempted connection string: postgresql://{creds_part.split(':')[0]}:***@{host_db_part.rsplit('/', 1)[0]}/postgres")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Setting up database...")
    if create_database():
        print("\n✓ Database setup complete!")
        print("You can now start the FastAPI server.")
    else:
        print("\n✗ Database setup failed!")
        sys.exit(1)

