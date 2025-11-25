# Setup Instructions for Login and Register

## Prerequisites

1. **PostgreSQL** must be installed and running
2. **Python 3.8+** installed
3. All Python dependencies installed

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Configure Environment

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
   (On Linux/Mac: `cp .env.example .env`)

2. Edit `.env` file and update:
   - `DATABASE_URL` - Your PostgreSQL connection string
   - `SECRET_KEY` - A secure random string for JWT tokens

## Step 3: Setup Database

Run the database setup script to create the database:

```bash
python setup_database.py
```

Or manually create the database:
```sql
CREATE DATABASE career_recommendations;
```

## Step 4: Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the provided run script:
```bash
run.bat
```

## Step 5: Test the Endpoints

### Register a new user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "John Doe", "email": "john@example.com", "password": "password123"}'
```

### Login:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=password123"
```

## Frontend Integration

The frontend is already configured to use:
- Register: `http://localhost:8000/auth/register`
- Login: `http://localhost:8000/auth/login`

Make sure the backend is running on port 8000 and the frontend on port 5173.

## Troubleshooting

### Database Connection Errors

1. Verify PostgreSQL is running:
   ```bash
   # Windows
   net start postgresql-x64-XX
   
   # Linux/Mac
   sudo systemctl status postgresql
   ```

2. Check database credentials in `.env` file

3. Ensure the database exists:
   ```bash
   python setup_database.py
   ```

### Import Errors

If you get import errors for `email-validator`:
```bash
pip install email-validator==2.1.0
```

### Port Already in Use

If port 8000 is already in use, change it in the uvicorn command or update the frontend URLs.



