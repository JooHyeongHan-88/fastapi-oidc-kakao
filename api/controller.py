import requests
import base64
import json
from typing import Optional

from api.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_SERVER, API_SERVER


def _decode64(string: str) -> Optional[None]:
    """
    Base64 디코딩 string 반환
    """
    string += '=' * ((4 - len(string) % 4) % 4)
    try:
        decoded_bytes = base64.b64decode(string)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        print("디코딩 오류:", e)
        return None
    

class OIDC:
    def __init__(self):
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        self.access_token = None
        self.refresh_token = None
        self.userinfo = None

    def auth(self, code: str) -> Optional[bool]:
        response = requests.post(
            url=AUTH_SERVER + "/oauth/token", 
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            }, 
        )
        if response.status_code == 200:
            token_info = response.json()
            
            self.access_token = token_info['access_token']
            self.refresh_token = token_info['refresh_token']
    
            id_token = token_info['id_token']
            _, payload, _ = id_token.split(".")
            self.userinfo = json.loads(_decode64(payload))

            return True
        
    def expire_token(self) -> Optional[bool]:
        response = requests.post(
            url=API_SERVER + "/v1/user/logout",
            headers={
                **self.default_header,
                **{"Authorization": "Bearer " + self.access_token}
            }
        )
        if response.status_code == 200:
            self.access_token = None
            self.refresh_token = None
            self.userinfo = None
            return True

    def logout(self) -> Optional[bool]:
        response = requests.get(url=f"{self.auth_server}/oauth/logout?client_id=${CLIENT_ID}&logout_redirect_uri=${REDIRECT_URI}")
        if response.status_code == 200:
            self.access_token = None
            self.refresh_token = None
            self.userinfo = None
            return True
        