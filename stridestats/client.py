import requests
from .auth import StravaAuth

class StravaClient:
    """
    Wrapper for the Strava V3 API.
    """
    BASE_URL = "https://www.strava.com/api/v3"

    def __init__(self, auth: StravaAuth):
        self.auth = auth

    def _get_headers(self):
        token = self.auth.get_access_token()
        return {"Authorization": f"Bearer {token}"}

    def _request(self, method, url, **kwargs):
        headers = self._get_headers()
        response = requests.request(method, url, headers=headers, **kwargs)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Try to get more detail from the response body
            try:
                error_data = response.json()
                print(f"Strava API Error: {error_data}")
            except:
                pass
            raise e
        return response.json()

    def get_athlete(self):
        url = f"{self.BASE_URL}/athlete"
        return self._request("GET", url)

    def get_activities(self, before=None, after=None, page=1, per_page=30):
        url = f"{self.BASE_URL}/athlete/activities"
        params = {
            'before': before,
            'after': after,
            'page': page,
            'per_page': per_page
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", url, params=params)
