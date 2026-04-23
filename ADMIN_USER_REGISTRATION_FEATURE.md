# Admin Login Feature - User Registration Table

## Overview
This feature enables admin users to log in and view a comprehensive table of all registered users with their encrypted passwords and login timestamps.

## Features Implemented

### 1. **Database Model Updates**
- Added `created_at` timestamp field to track user registration date
- Added `last_login` timestamp field to track the last login time of each user
- The User model now includes:
  - `id`: User ID (Primary Key)
  - `full_name`: User's full name
  - `email`: User's email (unique, indexed)
  - `password`: Encrypted password hash (bcrypt)
  - `is_admin`: Boolean flag for admin status
  - `created_at`: Registration timestamp (auto-set)
  - `last_login`: Last login timestamp (nullable, updated on login)

### 2. **Backend Authentication Updates**
- **Login Timestamp Recording**: When a user logs in via `/login` endpoint, the `last_login` field is automatically updated with the current UTC timestamp
- **Password Security**: Passwords are stored as bcrypt hashes, ensuring they are never stored in plaintext
- **Admin Authorization**: The admin endpoints require the user to have `is_admin=true` flag

### 3. **New Admin API Endpoint**
- **Endpoint**: `GET /admin/users/details/all`
- **Authentication**: Requires valid JWT token with admin status
- **Response**: Returns a list of all users including:
  - User ID
  - Full Name
  - Email
  - Encrypted Password (bcrypt hash - for reference only)
  - Admin Status
  - Created At (Registration Date & Time)
  - Last Login (Last Login Date & Time, or null if never logged in)

### 4. **Frontend Admin Dashboard Enhancements**
The Admin Dashboard now displays a comprehensive user registration table with the following columns:

| Column | Description |
|--------|-------------|
| ID | Unique user identifier |
| Full Name | User's full name |
| Email | User's email address |
| Encrypted Password | First 20 characters of the bcrypt hash (hover for full hash) |
| Registration Date | Date and time when the user registered |
| Last Login | Date and time of the user's last login (or "Never" if never logged in) |
| Admin | Shows "Yes" or "No" indicating admin status |
| Actions | Edit and Delete buttons |

### 5. **User Registration Flow**
When a user registers via `/register` endpoint:
1. Password is hashed using bcrypt
2. User record is created with `created_at` set to current UTC time
3. `last_login` is initially set to NULL

### 6. **User Login Flow**
When a user logs in via `/login` endpoint:
1. Email and password are validated
2. Password is verified against the bcrypt hash
3. `last_login` is updated to current UTC time
4. JWT token is issued for session management

## Database Migration

A migration file has been created to add the new columns to the User table:
- **File**: `backend/alembic/versions/add_user_timestamps.py`
- **Columns Added**:
  - `created_at` (DateTime, NOT NULL, default: current timestamp)
  - `last_login` (DateTime, nullable)
  - `is_admin` (Boolean, default: False)

To run the migration:
```bash
cd backend
alembic upgrade head
```

## API Usage Examples

### Admin Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin_password"
```

### Get All Users with Details
```bash
curl -X GET "http://localhost:8000/admin/users/details/all" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Regular User Registration
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

## Security Considerations

1. **Password Security**: All passwords are hashed using bcrypt before storage. The encrypted hashes shown in the admin dashboard are for reference only.
2. **Admin Authorization**: The user registration table is only accessible to users with `is_admin=true` flag
3. **JWT Tokens**: Session tokens are signed with a secret key and have an expiration time
4. **HTTPS Recommended**: In production, all endpoints should be served over HTTPS

## Files Modified

### Backend
- `backend/app/database/models.py` - Added timestamp fields to User model
- `backend/app/api/routers/auth.py` - Added login timestamp recording
- `backend/app/api/routers/admin.py` - Added new endpoint for user details with passwords and login times
- `backend/alembic/versions/add_user_timestamps.py` - New migration file

### Frontend
- `frontend/src/pages/AdminDashboard.jsx` - Updated to display new user table with encrypted passwords and login times

## Configuration

### Environment Variables (in `.env`)
```
ADMIN_EMAIL=admin@careerpath.com
ADMIN_PASSWORD=admin123
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
```

### Making a User an Admin

To make a user an admin, update the database directly:
```sql
UPDATE "user" SET is_admin = true WHERE id = 1;
```

Or create an admin registration endpoint if needed.

## Testing the Feature

1. **Register a user** via the registration endpoint
2. **Log in as admin** using the admin credentials from `.env`
3. **Navigate to Admin Dashboard**
4. **View the Users tab** to see all registered users with:
   - Encrypted passwords
   - Registration dates
   - Last login times

## Future Enhancements

- Add password reset functionality
- Implement role-based access control (RBAC)
- Add user activity logging
- Create reports based on login patterns
- Add email verification for new registrations
- Implement two-factor authentication (2FA) for admin accounts
