import requests
import json

# Client ID and client secret obtained from Strava developer dashboard
client_id = 116557
client_secret = "27b89fbdfc1a0168c201c988dfa4bd05c174c9da"

# Authorization URL
authorization_url = "https://www.strava.com/oauth/authorize"

# Redirect URI specified in Strava developer dashboard
redirect_uri = "http://localhost:5000"

# Scope for the API request
scope = "activity:write,read"

# Authorization parameters
params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",
    "scope": scope
}

# Generate authorization URL
authorization_url = requests.Request('GET', authorization_url, params=params).url

# Print the authorization URL
print(f"Authorization URL: {authorization_url}")

# Redirect the user to the authorization URL to grant access
# Paste the authorization code from the redirect URL into the code below
authorization_code = input("Enter authorization code: ")

# Exchange authorization code for access token
token_url = "https://www.strava.com/oauth/token"

# Request parameters
token_params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri
}

# Send request to exchange authorization code for access token
token_response = requests.post(token_url, data=token_params)

# Check if the request was successful
if token_response.status_code == 200:
    # Parse JSON response
    token_data = json.loads(token_response.text)

    # Access token is stored in the 'access_token' key
    access_token = token_data["access_token"]

    # Print the access token
    print(f"Access token: {access_token}")
else:
    # Handle error
    print("Error retrieving access token")
