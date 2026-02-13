import requests
import time
import sys
import uuid

BASE_URL = "http://127.0.0.1:8000"
AUTH_URL = f"{BASE_URL}/api/v1/auth"
WALLETS_URL = f"{BASE_URL}/api/v1/wallets"

def print_step(msg):
    print(f"\n{'='*50}\n{msg}\n{'='*50}")

def verify_monolith():
    print_step("STARTING MONOLITH VERIFICATION")
    
    # 1. Check Health (if endpoint exists) or just root
    try:
        resp = requests.get(f"{BASE_URL}/admin/login/", timeout=5)
        print(f"Server is reachable: {resp.status_code}")
    except Exception as e:
        print(f"Server NOT reachable: {e}")
        return False

    # 2. Register/Login User A
    email_a = f"user_a_{uuid.uuid4().hex[:8]}@example.com"
    password = "Password123!"
    print_step(f"Registering User A: {email_a}")
    
    resp = requests.post(f"{AUTH_URL}/register/", json={
        "email": email_a,
        "password": password,
        "first_name": "User",
        "last_name": "A"
    })
    if resp.status_code != 201:
        print(f"Registration failed: {resp.text}")
        # Try login if already exists (unlikely with uuid)
    
    print("Logging in User A...")
    resp = requests.post(f"{AUTH_URL}/login/", json={
        "email": email_a,
        "password": password
    })
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return False
    
    token_a = resp.json()['access']
    headers_a = {"Authorization": f"Bearer {token_a}"}
    print("User A logged in.")

    # 3. Create Wallet for User A (BIF)
    print_step("Creating BIF Wallet for User A")
    resp = requests.post(f"{WALLETS_URL}/", json={
        "currency": "BIF",
        "wallet_type": "PERSONAL",
        "name": "My BIF Wallet"
    }, headers=headers_a)
    
    if resp.status_code != 201:
        print(f"Wallet creation failed: {resp.text}")
        return False
    
    wallet_a = resp.json()
    wallet_a_id = wallet_a['id']
    print(f"Wallet A created: {wallet_a_id} ({wallet_a['currency']})")

    # 4. Check Balance A
    print(f"Initial Balance A: {wallet_a['balance']}")

    # 5. Register/Login User B
    email_b = f"user_b_{uuid.uuid4().hex[:8]}@example.com"
    print_step(f"Registering User B: {email_b}")
    
    resp = requests.post(f"{AUTH_URL}/register/", json={
        "email": email_b,
        "password": password,
        "first_name": "User",
        "last_name": "B"
    })
    
    resp = requests.post(f"{AUTH_URL}/login/", json={
        "email": email_b,
        "password": password
    })
    token_b = resp.json()['access']
    headers_b = {"Authorization": f"Bearer {token_b}"}
    print("User B logged in.")

    # 6. Create Wallet for User B (BIF)
    print_step("Creating BIF Wallet for User B")
    resp = requests.post(f"{WALLETS_URL}/", json={
        "currency": "BIF", 
        "wallet_type": "PERSONAL",
        "name": "B's Wallet"
    }, headers=headers_b)
    
    wallet_b = resp.json()
    wallet_b_id = wallet_b['id']
    print(f"Wallet B created: {wallet_b_id}")

    # 7. Credit Wallet A (Internal/Admin endpoint or similar? No, only admin)
    # Since we can't easily credit via API without admin, we might skip transfer test 
    # OR we use the admin endpoint if we can authenticate as admin.
    # For now, let's just verify wallet creation and list.
    
    print_step("Listing Wallets for User A")
    resp = requests.get(f"{WALLETS_URL}/", headers=headers_a)
    print(f"User A Wallets: {len(resp.json())}")
    
    return True

if __name__ == "__main__":
    if verify_monolith():
        print("\nSUCCESS: Monolith verification passed!")
        sys.exit(0)
    else:
        print("\nFAILURE: Monolith verification failed.")
        sys.exit(1)
