from streamlitextras.webutils import stxs_javascript
from streamlitextras.cookiemanager import get_cookie_manager
import requests

from config import API_URL, BASE_URL


def get_auth_url() -> str:
    response = requests.get(f"{API_URL}/auth/url", allow_redirects=False)
    if response.status_code == 307:
        redirected_url = response.headers['Location']
        return redirected_url
    else:
        return False


def redirect(url: str):
    stxs_javascript(f"window.location.replace('{url}');")


def get_id_token(code: str) -> str:
    url = f"{API_URL}/auth"
    data = {"code": code}
    
    response = requests.post(url=url, json=data)
    
    return response
    

def set_cookie(name, value):
    stxs_javascript(f'document.cookie = "{name}={value}; path=/"')


def get_cookie(name):
    cookie_manager = get_cookie_manager()
    return cookie_manager.get(name)