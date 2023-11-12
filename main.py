from flask import Flask, redirect, url_for, request, session, render_template
import requests
import json

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Client ID and client secret obtained from Strava developer dashboard
client_id = 116557
client_secret = "27b89fbdfc1a0168c201c988dfa4bd05c174c9da"

# Redirect URI specified in Strava developer dashboard
redirect_uri = "http://localhost:5000"

# Scope for the API request
scope = "activity:write,read_all"


@app.route("/login")
def index():
    # Authorization URL
    authorization_url = "https://www.strava.com/oauth/authorize"

    # Authorization parameters
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope
    }

    # Generate authorization URL
    authorization_url = requests.Request('GET', authorization_url, params=params)
    r = authorization_url.prepare()

    return redirect(r.url)


@app.route("/")
def authorized():
    # Exchange authorization code for access token
    token_url = "https://www.strava.com/oauth/token"

    # Retrieve the authorization code from the URL query parameter
    authorization_code = request.args.get('code')

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

        # Store the access token in the session for future use
        session['access_token'] = access_token

        # Display a message indicating successful authorization
        return "Successfully authorized with Strava"
    else:
        # Handle error
        return "Error retrieving access token"


@app.route("/get_data")
def get_data():
    token = session['access_token']
    headers = {"Authorization": "Bearer " + token}
    r = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)
    print(r)
    return render_template("athlete.html", data=r.json())


if __name__ == "__main__":
    app.run(debug=True)
