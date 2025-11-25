# Admin Setup Guide

## Creating Admin User

To create the admin user in the database, run:

```bash
cd backend
python app/database/create_admin.py
```

This will create an admin user with:
- **Email**: `admin@careerpath.com` (configurable in `.env`)
- **Password**: `admin123` (configurable in `.env`)

## Default Admin Credentials

- **Email**: `admin@careerpath.com`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change these credentials in production by updating the `.env` file:

```
ADMIN_EMAIL=your-admin-email@example.com
ADMIN_PASSWORD=your-secure-password
```

## Admin Features

Once logged in as admin, you can:

1. **View All Users**: See all registered users in the system
2. **View All Predictions**: See all career predictions made by users
3. **Edit Users**: Update user names and emails
4. **Delete Users**: Remove users from the system
5. **Delete Predictions**: Remove predictions from the system

## Accessing Admin Dashboard

1. Click "Admin" button in the navbar (red button)
2. Login with admin credentials
3. You'll be redirected to the admin dashboard

## API Endpoints

All admin endpoints require authentication and admin privileges:

- `GET /admin/users` - Get all users
- `GET /admin/predictions` - Get all predictions
- `DELETE /admin/users/{user_id}` - Delete a user
- `DELETE /admin/predictions/{prediction_id}` - Delete a prediction
- `PUT /admin/users/{user_id}` - Update a user
- `PUT /admin/predictions/{prediction_id}` - Update a prediction



