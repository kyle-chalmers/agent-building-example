"""
Test script to check Thingiverse API connectivity and functionality.
"""

import os
import requests
from thingiverse_client import ThingiverseClient

def test_api_connectivity():
    """Test basic API connectivity without authentication"""
    print("=" * 60)
    print("Testing Thingiverse API Connectivity")
    print("=" * 60)
    
    base_url = "https://api.thingiverse.com"
    
    # Test 1: Check if API is reachable
    print("\n1. Testing API endpoint reachability...")
    try:
        # Try to access the developers page (not API, but related)
        response = requests.get("https://www.thingiverse.com/developers", timeout=10)
        print(f"   ✓ Developers page is reachable (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Cannot reach Thingiverse: {e}")
        return False
    
    # Test 2: Try an API endpoint without token
    print("\n2. Testing API endpoint (without token)...")
    try:
        response = requests.get(f"{base_url}/newest", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ API endpoint is working (requires access token)")
        elif response.status_code == 200:
            print("   ✓ API endpoint is accessible (may not require token for some endpoints)")
        else:
            print(f"   Response: {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"   Error: {e}")
    
    # Test 3: Check if we have credentials
    print("\n3. Checking for API credentials...")
    access_token = os.getenv("THINGIVERSE_ACCESS_TOKEN")
    if access_token:
        print(f"   ✓ Found THINGIVERSE_ACCESS_TOKEN (length: {len(access_token)})")
        
        # Test 4: Try to initialize client
        print("\n4. Testing client initialization...")
        try:
            client = ThingiverseClient(access_token=access_token)
            print("   ✓ Client initialized successfully")
        except Exception as e:
            print(f"   ✗ Error initializing client: {e}")
            return False
        
        # Test 5: Try a simple API call
        print("\n5. Testing API call (get newest things)...")
        try:
            results = client.get_newest(per_page=3)
            print(f"   ✓ API call successful!")
            print(f"   Retrieved {len(results)} things")
            if results:
                print(f"   First thing: {results[0].get('name', 'N/A')} (ID: {results[0].get('id', 'N/A')})")
        except requests.exceptions.HTTPError as e:
            print(f"   ✗ HTTP Error: {e}")
            if e.response:
                print(f"   Status: {e.response.status_code}")
                print(f"   Response: {e.response.text[:200]}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Test 6: Try to get a specific thing
        print("\n6. Testing get thing details...")
        try:
            # Use a known thing ID (example: 4002927 from documentation)
            thing_id = 4002927
            thing = client.get_thing(thing_id)
            print(f"   ✓ Retrieved thing: {thing.get('name', 'N/A')}")
        except requests.exceptions.HTTPError as e:
            print(f"   Status: {e.response.status_code if e.response else 'N/A'}")
            if e.response and e.response.status_code == 404:
                print("   (Thing not found - this is expected if ID doesn't exist)")
            else:
                print(f"   Response: {e.response.text[:200] if e.response else 'N/A'}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 7: Try search
        print("\n7. Testing search functionality...")
        try:
            results = client.search_things(query="test", per_page=3)
            print(f"   ✓ Search successful!")
            print(f"   Found {len(results)} results")
        except requests.exceptions.HTTPError as e:
            print(f"   Status: {e.response.status_code if e.response else 'N/A'}")
            print(f"   Response: {e.response.text[:200] if e.response else 'N/A'}")
        except Exception as e:
            print(f"   Error: {e}")
    else:
        print("   ✗ THINGIVERSE_ACCESS_TOKEN not found")
        print("   To test with credentials:")
        print("   1. Get an access token (see GETTING_CREDENTIALS.md)")
        print("   2. Set: export THINGIVERSE_ACCESS_TOKEN='your-access-token'")
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    test_api_connectivity()
