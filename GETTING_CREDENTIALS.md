# How to Obtain Thingiverse API Credentials

## Overview

The Thingiverse API uses OAuth 2.0 for authentication. You need to create a Web App and obtain an access token to use the API.

## Steps to Get API Access

### 1. Create a Thingiverse Account

If you don't already have one:
- Visit https://www.thingiverse.com/
- Click "Sign Up" to create a free account
- Verify your email address

### 2. Create a Web App

1. **Visit the Developers Portal**
   - Go to https://www.thingiverse.com/developers/getting-started
   - Log in with your Thingiverse account

2. **Create a New App**
   - Click "Create a new app" or similar button
   - Fill in the required information:
     - **App Name**: Choose a name for your application
     - **Description**: Describe what your app does
     - **Redirect URI**: For read-only access, you can use `http://localhost` or `urn:ietf:wg:oauth:2.0:oob`
     - **Permissions**: Select the permissions you need (read, write, etc.)

3. **Get Your Client ID**
   - After creating the app, you'll receive a **Client ID**
   - Save this Client ID for the next step

### 3. Obtain an Access Token

There are two methods to get an access token:

#### Method A: OAuth Authorization Flow (Recommended)

1. **Construct the Authorization URL**
   ```
   https://www.thingiverse.com/login/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=token
   ```
   Replace `YOUR_CLIENT_ID` with the Client ID from step 2.

2. **Authorize the App**
   - Open the URL in your web browser
   - Log in to Thingiverse if prompted
   - Grant permission to your app when asked

3. **Extract the Access Token**
   - After authorization, you'll be redirected to a URL like:
     ```
     http://localhost#access_token=YOUR_ACCESS_TOKEN&token_type=bearer&expires_in=3600
     ```
   - Copy the `access_token` value from the URL
   - This is your access token!

#### Method B: Read-Only App Token (If Available)

Some accounts may have access to read-only app tokens:
- Check the Thingiverse developers portal for "App Token" or "Read-Only Token"
- This may be simpler for basic read operations

### 4. Set Your Access Token

Once you have your access token, set it as an environment variable:

```bash
export THINGIVERSE_ACCESS_TOKEN="your-access-token-here"
```

Or use it directly in your code:

```python
from thingiverse_client import ThingiverseClient

client = ThingiverseClient(access_token="your-access-token-here")
```

## Important Notes

- **Token Expiration**: Access tokens may expire. Check the `expires_in` parameter from the OAuth response.
- **Token Refresh**: You may need to repeat the OAuth flow to get a new token when it expires.
- **Rate Limits**: The API may have rate limits. Check the API documentation for current limits.
- **Permissions**: Make sure your app has the necessary permissions for the operations you want to perform.

## Testing Your Credentials

1. Set the access token:
   ```bash
   export THINGIVERSE_ACCESS_TOKEN="your-access-token-here"
   ```

2. Run the test script:
   ```bash
   source venv/bin/activate  # if using virtual environment
   python test_api.py
   ```

3. Or use the example script:
   ```bash
   python example_usage.py
   ```

## Troubleshooting

### "Invalid access token" Error

- Verify your token is correct (no extra spaces or characters)
- Check if the token has expired
- Make sure you're using the full token string

### "401 Unauthorized" Error

- Your access token may be invalid or expired
- Try obtaining a new token using the OAuth flow
- Verify your app has the correct permissions

### "404 Not Found" Error

- The thing ID or resource may not exist
- Check that you're using the correct API endpoint
- Verify the thing is public (private things may not be accessible)

## Additional Resources

- **API Documentation**: https://www.thingiverse.com/developers
- **Getting Started Guide**: https://www.thingiverse.com/developers/getting-started
- **Thingiverse Community**: https://www.thingiverse.com/

## Questions?

If you encounter issues:
- Check the Thingiverse API documentation
- Review the error messages from the API
- Contact Thingiverse support if needed
- Check the GitHub issues for the official Thingiverse API libraries
