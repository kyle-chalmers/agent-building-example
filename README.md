# Thingiverse API Client

A Python client for interacting with the Thingiverse API. This client provides easy access to search, browse, and download 3D models from Thingiverse.

## Features

- 🔍 Search things by query string
- 📦 Browse newest and popular things
- 📋 Get detailed thing information
- 📁 Access thing files (STL, OBJ, STEP, etc.)
- 🖼️ Get thing images and thumbnails
- 👤 Access user profiles and their things
- ⬇️ Download files from Thingiverse

## Installation

```bash
pip install -r requirements.txt
```

## Getting Started

### 1. Obtain API Credentials

To use the API, you need an **access token** from Thingiverse:

1. Visit https://www.thingiverse.com/developers/getting-started
2. Create a Web App to get a Client ID
3. Follow the OAuth flow to obtain an access token

See `GETTING_CREDENTIALS.md` for detailed instructions.

### 2. Set Your Access Token

**Option 1: Environment Variable (Recommended)**
```bash
export THINGIVERSE_ACCESS_TOKEN="your-access-token-here"
```

**Option 2: Pass Directly**
```python
client = ThingiverseClient(access_token="your-access-token-here")
```

### 3. Basic Usage

```python
from thingiverse_client import ThingiverseClient

# Initialize client
client = ThingiverseClient(access_token="your-access-token")

# Get newest things
newest = client.get_newest(per_page=10)
print(f"Found {len(newest)} things")

# Get thing details
thing_id = newest[0]['id']
details = client.get_thing(thing_id)
print(f"Thing: {details['name']}")

# Get files for a thing
files = client.get_thing_files(thing_id)
print(f"Files: {len(files)}")
```

## API Methods

### Things
- `get_newest(per_page, page)` - Get newest things
- `get_popular(per_page, page)` - Get popular things
- `get_thing(thing_id)` - Get thing details by ID
- `get_thing_files(thing_id)` - Get files for a thing
- `get_thing_images(thing_id)` - Get images for a thing
- `get_thing_tags(thing_id)` - Get tags for a thing

### Search
- `search_things(query, per_page, page)` - Search things by query

### Users
- `get_user(username)` - Get user profile
- `get_user_things(username, per_page, page)` - Get things by user

### Downloads
- `download_file(file_url, save_path)` - Download file to disk

## Example Script

Run the example script to see the API in action:

```bash
export THINGIVERSE_ACCESS_TOKEN="your-access-token"
python example_usage.py
```

## Supported File Formats

Thingiverse supports various 3D printing and CAD formats:
- **3D Formats**: STL, OBJ, 3MF, STEP, SLDPRT, SLDASM, IGES, X_T, IPT, PRT
- **2D Formats**: SVG, PDF, PNG, JPG
- **Other**: ZIP (archives), GCODE (printer files)

## API Documentation

Full API documentation available at:
- Developers Portal: https://www.thingiverse.com/developers
- Getting Started: https://www.thingiverse.com/developers/getting-started
- API Base: https://api.thingiverse.com/

## Error Handling

The client uses `requests` and will raise exceptions for HTTP errors:
- `401 Unauthorized` - Invalid or expired access token
- `404 Not Found` - Thing or resource not found
- `400 Bad Request` - Invalid parameters
- `429 Too Many Requests` - Rate limit exceeded

Handle errors appropriately in your code:

```python
try:
    results = client.get_newest(per_page=10)
except requests.exceptions.HTTPError as e:
    print(f"API Error: {e}")
    if e.response.status_code == 401:
        print("Invalid or expired access token")
```

## Testing

Test API connectivity and functionality:

```bash
export THINGIVERSE_ACCESS_TOKEN="your-access-token"
python test_api.py
```

## Notes

- Access tokens are obtained through OAuth 2.0 flow
- Tokens may expire; you'll need to refresh them
- Some endpoints may have rate limits
- File downloads require the access token in the URL

## License

This client is provided as-is for use with the Thingiverse API.
