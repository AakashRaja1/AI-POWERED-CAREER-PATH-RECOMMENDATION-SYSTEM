"""
Simple test script to verify authentication endpoints work.
Run this after starting the server.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    print("Testing registration...")
    url = f"{BASE_URL}/auth/register"
    data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("✓ Registration successful!")
            print(f"  User ID: {response.json()['id']}")
            print(f"  Email: {response.json()['email']}")
            return True
        else:
            print(f"✗ Registration failed: {response.status_code}")
            print(f"  Error: {response.json()}")
            return False
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\nTesting login...")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            print("✓ Login successful!")
            print(f"  Token type: {token_data['token_type']}")
            print(f"  Access token: {token_data['access_token'][:50]}...")
            return token_data['access_token']
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"  Error: {response.json()}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def test_duplicate_registration():
    """Test that duplicate email registration fails"""
    print("\nTesting duplicate registration...")
    url = f"{BASE_URL}/auth/register"
    data = {
        "full_name": "Another User",
        "email": "test@example.com",  # Same email
        "password": "differentpassword"
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 400:
            print("✓ Duplicate registration correctly rejected!")
            return True
        else:
            print(f"✗ Duplicate registration should have failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_wrong_password():
    """Test login with wrong password"""
    print("\nTesting wrong password...")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "test@example.com",
        "password": "wrongpassword"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 401:
            print("✓ Wrong password correctly rejected!")
            return True
        else:
            print(f"✗ Wrong password should have failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Authentication Endpoint Tests")
    print("=" * 50)
    print("\nMake sure the server is running on http://localhost:8000")
    print()
    
    # Test registration
    if test_register():
        # Test duplicate registration
        test_duplicate_registration()
        
        # Test login
        token = test_login()
        
        # Test wrong password
        test_wrong_password()
        
        if token:
            print("\n" + "=" * 50)
            print("✓ All tests passed!")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("✗ Some tests failed")
            print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("✗ Initial registration failed - check server and database")
        print("=" * 50)



