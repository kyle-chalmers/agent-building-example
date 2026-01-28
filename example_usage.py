"""
Example usage of the Thingiverse API client.

Before running, set your access token:
1. Get an access token from Thingiverse (see GETTING_CREDENTIALS.md)
2. Set it as an environment variable: export THINGIVERSE_ACCESS_TOKEN="your-access-token"
3. Or pass it directly when creating the client
"""

import os
from thingiverse_client import ThingiverseClient


def main():
    # Initialize client
    # Option 1: Use environment variable
    access_token = os.getenv("THINGIVERSE_ACCESS_TOKEN")
    
    # Option 2: Pass directly (not recommended for production)
    # access_token = "your-access-token-here"
    
    if not access_token:
        print("Error: THINGIVERSE_ACCESS_TOKEN environment variable not set")
        print("Please set it with: export THINGIVERSE_ACCESS_TOKEN='your-access-token'")
        print("See GETTING_CREDENTIALS.md for instructions on obtaining a token")
        return
    
    client = ThingiverseClient(access_token=access_token)
    
    print("=" * 60)
    print("Thingiverse API Example")
    print("=" * 60)
    
    # Example 1: Get newest things
    print("\n1. Getting newest things...")
    try:
        newest = client.get_newest(per_page=5)
        print(f"   Found {len(newest)} things:\n")
        
        for thing in newest:
            print(f"   - ID: {thing.get('id', 'N/A')}")
            print(f"     Name: {thing.get('name', 'N/A')}")
            print(f"     Creator: {thing.get('creator', {}).get('name', 'N/A')}")
            print(f"     URL: {thing.get('public_url', 'N/A')}")
            print()
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Get thing details
    if newest:
        thing_id = newest[0].get('id')
        if thing_id:
            print(f"\n2. Getting details for thing ID {thing_id}...")
            try:
                details = client.get_thing(thing_id)
                print(f"   Name: {details.get('name', 'N/A')}")
                print(f"   Description: {details.get('description', 'N/A')[:100]}...")
                print(f"   Added: {details.get('added', 'N/A')}")
                print(f"   Modified: {details.get('modified', 'N/A')}")
                print(f"   Published: {details.get('is_published', False)}")
            except Exception as e:
                print(f"   Error: {e}")
    
    # Example 3: Get thing files
    if newest and thing_id:
        print(f"\n3. Getting files for thing ID {thing_id}...")
        try:
            files = client.get_thing_files(thing_id)
            print(f"   Found {len(files)} files:")
            for file in files[:5]:  # Show first 5 files
                print(f"   - {file.get('name', 'N/A')} ({file.get('size', 'N/A')} bytes)")
        except Exception as e:
            print(f"   Error: {e}")
    
    # Example 4: Search for things
    print("\n4. Searching for 'motor mount'...")
    try:
        search_results = client.search_things(query="motor mount", per_page=5)
        print(f"   Found {len(search_results)} results:")
        for thing in search_results[:3]:  # Show first 3
            print(f"   - {thing.get('name', 'N/A')} (ID: {thing.get('id', 'N/A')})")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 5: Get popular things
    print("\n5. Getting popular things...")
    try:
        popular = client.get_popular(per_page=3)
        print(f"   Found {len(popular)} popular things:")
        for thing in popular:
            print(f"   - {thing.get('name', 'N/A')} by {thing.get('creator', {}).get('name', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 6: Download file (commented out - requires valid file URL)
    # if newest and thing_id:
    #     print(f"\n6. Downloading a file from thing ID {thing_id}...")
    #     try:
    #         files = client.get_thing_files(thing_id)
    #         if files:
    #             # Find an STL file
    #             stl_file = next((f for f in files if f.get('name', '').endswith('.stl')), None)
    #             if stl_file:
    #                 download_url = stl_file.get('download_url') or stl_file.get('url')
    #                 if download_url:
    #                     client.download_file(download_url, "downloaded_model.stl")
    #                     print(f"   Downloaded: {stl_file.get('name')}")
    #     except Exception as e:
    #         print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
