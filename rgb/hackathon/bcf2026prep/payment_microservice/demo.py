"""
Demo script to demonstrate Payment Microservice functionality.
Run this script while the server is running on http://localhost:5001
"""
import requests
import jwt
import datetime
import json

BASE_URL = "http://localhost:5001"
JWT_SECRET = "your-jwt-secret-key-must-match-auth-service"  # From .env

def create_test_token(user_id, email, is_verified=True):
    """Create a test JWT token (simulating auth microservice)."""
    payload = {
        "sub": user_id,
        "email": email,
        "is_verified": is_verified,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def demo():
    print("\n" + "🚀 PAYMENT MICROSERVICE DEMO 🚀".center(60))
    
    # 1. Health Check (No auth required)
    print("\n\n" + "="*60)
    print("1️⃣  HEALTH CHECKS (No Authentication Required)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print_response("Basic Health Check - GET /health", response)
    
    response = requests.get(f"{BASE_URL}/health/ready")
    print_response("Readiness Check - GET /health/ready", response)
    
    response = requests.get(f"{BASE_URL}/health/live")
    print_response("Liveness Check - GET /health/live", response)
    
    # 2. Test without token (should fail)
    print("\n\n" + "="*60)
    print("2️⃣  AUTHENTICATION TEST")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/payments")
    print_response("Without Token - GET /api/payments (Should fail 401)", response)
    
    # 3. Create test tokens
    token_user1 = create_test_token("user_123", "john@example.com", True)
    token_user2 = create_test_token("user_456", "jane@example.com", True)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}
    headers_user2 = {"Authorization": f"Bearer {token_user2}"}
    
    print(f"\n✅ Created JWT tokens for test users")
    
    # 4. Create Payments
    print("\n\n" + "="*60)
    print("3️⃣  CREATE PAYMENTS - POST /api/payments")
    print("="*60)
    
    # Create payment 1
    payment_data = {
        "booking_id": "BOOK-001",
        "amount": 150.00,
        "currency": "USD",
        "payment_method": "credit_card"
    }
    response = requests.post(f"{BASE_URL}/api/payments", json=payment_data, headers=headers_user1)
    print_response("Create Payment #1 (User 1)", response)
    payment1_id = response.json().get("payment", {}).get("payment_id") if response.ok else None
    
    # Create payment 2
    payment_data = {
        "booking_id": "BOOK-002",
        "amount": 275.50,
        "currency": "USD",
        "payment_method": "paypal"
    }
    response = requests.post(f"{BASE_URL}/api/payments", json=payment_data, headers=headers_user1)
    print_response("Create Payment #2 (User 1)", response)
    payment2_id = response.json().get("payment", {}).get("payment_id") if response.ok else None
    
    # Create payment for user 2
    payment_data = {
        "booking_id": "BOOK-003",
        "amount": 99.99,
        "currency": "EUR"
    }
    response = requests.post(f"{BASE_URL}/api/payments", json=payment_data, headers=headers_user2)
    print_response("Create Payment #3 (User 2)", response)
    
    # 5. Get User's Payments
    print("\n\n" + "="*60)
    print("4️⃣  GET USER'S PAYMENTS - GET /api/payments")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/payments", headers=headers_user1)
    print_response("Get All Payments (User 1 - should see 2)", response)
    
    response = requests.get(f"{BASE_URL}/api/payments", headers=headers_user2)
    print_response("Get All Payments (User 2 - should see 1)", response)
    
    # 6. Get Single Payment
    print("\n\n" + "="*60)
    print("5️⃣  GET SINGLE PAYMENT - GET /api/payments/<id>")
    print("="*60)
    
    if payment1_id:
        response = requests.get(f"{BASE_URL}/api/payments/{payment1_id}", headers=headers_user1)
        print_response(f"Get Payment by ID (Owner)", response)
        
        # Try to access another user's payment
        response = requests.get(f"{BASE_URL}/api/payments/{payment1_id}", headers=headers_user2)
        print_response(f"Get Payment by ID (Not Owner - should fail 403)", response)
    
    # 7. Get Payments by Booking
    print("\n\n" + "="*60)
    print("6️⃣  GET PAYMENTS BY BOOKING - GET /api/payments/booking/<id>")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/payments/booking/BOOK-001", headers=headers_user1)
    print_response("Get Payments for Booking BOOK-001", response)
    
    # 8. Process Payment
    print("\n\n" + "="*60)
    print("7️⃣  PROCESS PAYMENT - POST /api/payments/<id>/process")
    print("="*60)
    
    if payment1_id:
        response = requests.post(f"{BASE_URL}/api/payments/{payment1_id}/process", headers=headers_user1)
        print_response("Process Payment (pending → completed)", response)
        
        # Try to process again
        response = requests.post(f"{BASE_URL}/api/payments/{payment1_id}/process", headers=headers_user1)
        print_response("Process Payment Again (should fail)", response)
    
    # 9. Refund Payment
    print("\n\n" + "="*60)
    print("8️⃣  REFUND PAYMENT - POST /api/payments/<id>/refund")
    print("="*60)
    
    if payment1_id:
        response = requests.post(f"{BASE_URL}/api/payments/{payment1_id}/refund", headers=headers_user1)
        print_response("Refund Completed Payment", response)
    
    if payment2_id:
        response = requests.post(f"{BASE_URL}/api/payments/{payment2_id}/refund", headers=headers_user1)
        print_response("Refund Pending Payment (should fail)", response)
    
    # 10. Validation Tests
    print("\n\n" + "="*60)
    print("9️⃣  VALIDATION TESTS")
    print("="*60)
    
    # Missing required field
    response = requests.post(f"{BASE_URL}/api/payments", json={"amount": 100}, headers=headers_user1)
    print_response("Missing booking_id (should fail 400)", response)
    
    # Invalid amount
    response = requests.post(f"{BASE_URL}/api/payments", json={"booking_id": "TEST", "amount": -50}, headers=headers_user1)
    print_response("Negative amount (should fail 400)", response)
    
    # 11. Final State
    print("\n\n" + "="*60)
    print("🔟  FINAL STATE - All User 1 Payments")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/payments", headers=headers_user1)
    print_response("Final Payments List", response)
    
    print("\n\n" + "✅ DEMO COMPLETE! ".center(60, "="))
    print("\nThe payment microservice supports:")
    print("  • JWT authentication from auth microservice")
    print("  • User isolation (users only see their payments)")
    print("  • Payment lifecycle: pending → processing → completed → refunded")
    print("  • Pagination for listing payments")
    print("  • Health checks for Kubernetes/load balancers")
    print("  • RabbitMQ events (when enabled)")

if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the server!")
        print("   Make sure the server is running:")
        print("   python run.py")
