import requests
import base64

from api.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


class OIDC:
    def __init__(self):
        self.auth_server = "https://kauth.kakao.com"
        self.api_server = "https://kapi.kakao.com"
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

    def auth(self, code):
        return requests.post(
            url=self.auth_server + "/oauth/token", 
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            }, 
        ).json()


def decode64(string: str):
    string += '=' * ((4 - len(string) % 4) % 4)
    try:
        decoded_bytes = base64.b64decode(string)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        print("디코딩 오류:", e)
        return None