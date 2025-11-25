# Quick Start Guide

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Setup Database
```bash
python setup_database.py
```

## 3. Start Server
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Or use the batch file:
```bash
run.bat
```

## 4. Test (Optional)
In another terminal:
```bash
python test_auth.py
```

## API Endpoints

### Register
- **URL**: `POST /auth/register`
- **Body**: 
  ```json
  {
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }
  ```

### Login
- **URL**: `POST /auth/login`
- **Body** (form-data):
  ```
  username=john@example.com
  password=password123
  ```

## Frontend
The frontend is already configured to use these endpoints. Just start it:
```bash
cd ../frontend
npm install
npm run dev
```

## Troubleshooting

1. **Database connection error**: Make sure PostgreSQL is running
2. **Import errors**: Run `pip install -r requirements.txt`
3. **Port in use**: Change port in uvicorn command or kill the process using port 8000



