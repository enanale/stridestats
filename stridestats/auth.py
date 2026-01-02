import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class StravaAuth:
    """
    Handles OAuth2 authentication with Strava, including initial authorization,
    token storage in .env, and automatic refreshing.
    """
    def __init__(self):
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.access_token = os.getenv("STRAVA_ACCESS_TOKEN")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.expires_at = int(os.getenv("STRAVA_EXPIRES_AT", 0))

    def is_token_expired(self):
        # Buffer of 60 seconds
        return time.time() > (self.expires_at - 60)

    def refresh_access_token(self):
        print("Refreshing access token...")
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        response = requests.post("https://www.strava.com/oauth/token", data=payload)
        response.raise_for_status()
        data = response.json()

        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.expires_at = data['expires_at']

        self._save_tokens()
        return self.access_token

    def get_authorization_url(self, port=8000):
        scope = "read,activity:read_all"
        redirect_uri = f"http://localhost:{port}"
        url = (
            f"https://www.strava.com/oauth/authorize?"
            f"client_id={self.client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}"
        )
        return url

    def exchange_code_for_token(self, code):
        print(f"Exchanging code {code} for token...")
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.post("https://www.strava.com/oauth/token", data=payload)
        response.raise_for_status()
        data = response.json()

        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.expires_at = data['expires_at']

        self._save_tokens()
        return data

    def _save_tokens(self):
        # Update .env file (simple implementation)
        # In a real app, we might use a dedicated token storage
        with open(".env", "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.startswith("STRAVA_ACCESS_TOKEN="):
                new_lines.append(f"STRAVA_ACCESS_TOKEN={self.access_token}\n")
            elif line.startswith("STRAVA_REFRESH_TOKEN="):
                new_lines.append(f"STRAVA_REFRESH_TOKEN={self.refresh_token}\n")
            elif line.startswith("STRAVA_EXPIRES_AT="):
                new_lines.append(f"STRAVA_EXPIRES_AT={self.expires_at}\n")
            else:
                new_lines.append(line)

        with open(".env", "w") as f:
            f.writelines(new_lines)

    def get_access_token(self):
        if self.is_token_expired():
            return self.refresh_access_token()
        return self.access_token

if __name__ == "__main__":
    auth = StravaAuth()
    try:
        token = auth.get_access_token()
        print(f"Token is valid. Access Token: {token[:10]}...")
    except Exception as e:
        print(f"Error during token validation/refresh: {e}")
        print("Make sure STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET are set in .env")
