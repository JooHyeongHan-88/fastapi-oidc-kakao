import requests
import base64
import json
from typing import Optional

from api.config import (
    CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,
    AUTH_SERVER, API_SERVER
)


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
    def __init__(self, code: str):
        self.code = code

        self.access_token = None
        self.refresh_token = None
        self.id_token = None

        self.userid = None
        self.nickname = None
        self.picture = None

    def get_auth(self) -> Optional[bool]:
        """
        auth code 인증 및 토큰 획득
        """
        url = AUTH_SERVER + "/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": self.code,
        } 

        response = requests.post(url=url, headers=headers, data=data)

        if response.status_code == 200:
            token_info = response.json()

            self.access_token = token_info['access_token']
            self.refresh_token = token_info['refresh_token']
            self.id_token = token_info['id_token']

            return True
    
    def set_userinfo(self) -> bool:
        """
        JWT(id token) 디코딩 -> userinfo 저장
        """
        _, payload, _ = self.id_token.split(".")
        userinfo = json.loads(_decode64(payload))
        
        self.userid = userinfo["sub"]
        self.nickname = userinfo["nickname"]
        self.picture = userinfo["picture"]
            
        return True
        

def expire_token(access_token: str) -> Optional[bool]:
    """
    발급한 토큰 만료
    """
    url = API_SERVER + "/v1/user/logout"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
        "Authorization": "Bearer " + access_token,
    }

    response = requests.post(url=url, headers=headers)
    
    if response.status_code == 200:
        return True