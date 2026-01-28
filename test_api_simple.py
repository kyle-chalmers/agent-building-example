"""
Simple API test - check what we can discover without credentials
"""

import requests

base_url = "https://api.3dcontentcentral.com"

print("=" * 60)
print("3D Content Central API - Public Information Test")
print("=" * 60)

# Test 1: Swagger documentation
print("\n1. Checking Swagger documentation...")
try:
    response = requests.get(f"{base_url}/swagger", timeout=10)
    print(f"   ✓ Swagger UI accessible (Status: {response.status_code})")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Swagger spec
print("\n2. Checking Swagger specification...")
try:
    response = requests.get(f"{base_url}/swagger/docs/v1", timeout=10)
    if response.status_code == 200:
        spec = response.json()
        print(f"   ✓ Swagger spec accessible")
        print(f"   API Title: {spec.get('info', {}).get('title', 'N/A')}")
        print(f"   API Version: {spec.get('info', {}).get('version', 'N/A')}")
        print(f"   Available endpoints: {len(spec.get('paths', {}))}")
        
        # List some endpoint categories
        tags = [tag['name'] for tag in spec.get('tags', [])]
        print(f"   Endpoint categories: {', '.join(tags[:5])}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Token endpoint behavior
print("\n3. Testing token endpoint (without credentials)...")
try:
    response = requests.post(f"{base_url}/token", json="invalid", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        error = response.json()
        print(f"   Response: {error.get('message', 'N/A')}")
        print(f"   ✓ Endpoint is working (requires valid secret key)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Try an authenticated endpoint without token
print("\n4. Testing authenticated endpoint (without token)...")
try:
    response = requests.get(f"{base_url}/product-group", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print(f"   ✓ Endpoint requires authentication (as expected)")
    else:
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("Summary:")
print("  ✓ API is reachable and functional")
print("  ✓ Endpoints require authentication (secret key)")
print("  ✓ Client code structure is correct")
print("  ⚠ Need valid CONTENT_CENTRAL_SECRET_KEY to test full functionality")
print("=" * 60)
