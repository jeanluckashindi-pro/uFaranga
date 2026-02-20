
import urllib.request
import urllib.parse
import urllib.error
import json
import base64

BASE_URL = "http://127.0.0.1:8000/api/v1"

def send_request(url, method="GET", data=None, headers={}):
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("Content-Type", "application/json")
        for k, v in headers.items():
            req.add_header(k, v)
        
        if data:
            data_bytes = json.dumps(data).encode("utf-8")
            req.data = data_bytes
        
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return status, json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except:
            return e.code, body
    except Exception as e:
        print(f"Network error: {e}")
        return 0, None

def print_result(step, status, body):
    print(f"\n# {step}")
    print(f"Status Code: {status}")
    if isinstance(body, dict):
        print(f"Response: {json.dumps(body, indent=2)}")
    else:
        print(f"Response: {body}")

try:
    # 1. Register a new user
    register_data = {
        "email": "testuser@ufaranga.com",
        "username": "testuser",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+25779000000",
        "country": "Burundi",
        "city": "Bujumbura"
    }
    
    # Try to register
    print("Trying to register...")
    status, body = send_request(f"{BASE_URL}/auth/register/", "POST", data=register_data)
    
    if status == 400 and isinstance(body, dict) and "email" in body: # Probably already exists
         print("User already exists, proceeding to login.")
    elif status == 201:
        print_result("Registration Successful", status, body)
    else:
        print_result("Registration Failed", status, body)

    # 2. Login to get tokens
    login_data = {
        "email": "testuser@ufaranga.com",
        "password": "Password123!"
    }
    status, body = send_request(f"{BASE_URL}/auth/login/", "POST", data=login_data)
    
    if status == 200:
        tokens = body
        access_token = tokens["access"]
        
        print_result("Login Successful", status, body)
        
        # 3. Access Protected Endpoint (Me)
        headers = {"Authorization": f"Bearer {access_token}"}
        status, body = send_request(f"{BASE_URL}/auth/me/", "GET", headers=headers)
        print_result("Protected Endpoint (Me) Access", status, body)
        
        # 4. Access Users List (should fail for normal user)
        status, body = send_request(f"{BASE_URL}/users/", "GET", headers=headers)
        print(f"\n# Users List Access (Admin only)")
        print(f"Status Code: {status} (403 expected for normal user)")
        
    else:
        print_result("Login Failed", status, body)

except Exception as e:
    print(f"Global Error: {e}")
