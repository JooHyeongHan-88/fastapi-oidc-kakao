import requests
from typing import Optional

from streamlitextras.webutils import stxs_javascript
from streamlitextras.cookiemanager import get_cookie_manager

from config import API_URL


def get_auth_url() -> Optional[str]:
    """
    API 서버로부터 redirection URL 반환
    :: API 서버에서 RedirectResponse를 주어서 일반적으로는
    :: URL 반환 필요 없이 redirection 되지만 프론트엔드가 파이썬이라
    :: 브라우저에서 URL 받아서 직접 redirection 필요
    """
    response = requests.get(f"{API_URL}/auth/redirect", allow_redirects=False)
    if response.status_code == 307:
        redirected_url = response.headers['Location']
        return redirected_url
    else:
        return None


def redirect(url: str) -> None:
    """
    redirection 수행 JS 코드 실행 (by. streamlit-extras)
    """
    stxs_javascript(f"window.location.replace('{url}');")


def get_userinfo(code: str) -> Optional[dict]:
    """
    API 서버에 id_token 반환 요청
    """
    response = requests.post(url=f"{API_URL}/auth", json={"code": code})
    if response.status_code == 200:
        return response.json()
    

def set_cookie(name, value) -> None:
    """
    쿠키 저장 JS 코드 실행 (by. streamlit-extras)
    """
    stxs_javascript(f'document.cookie = "{name}={value}; path=/"')


def get_cookie(name) -> str:
    """
    쿠키 불러오기 JS 코드 실행 (by. streamlit-extras)
    """
    cookie_manager = get_cookie_manager()
    return cookie_manager.get(name)


def delete_cookie(name) -> None:
    """
    쿠키 삭제 JS 코드 실행 (by. streamlit-extras)
    """
    stxs_javascript(f"document.cookie = '{name}=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';")


def logout_cookie() -> Optional[bool]:
    """
    로그아웃 (쿠키 삭제)
    """
    delete_cookie("user")
    return True


def logout_expire() -> Optional[bool]:
    """
    로그아웃 (토큰 만료)
    """
    delete_cookie("user")
    response = requests.get(f"{API_URL}/logout/token")
    if response.status_code == 200:
        return True
    return True
    

def logout_account() -> None:
    """
    로그아웃 (카카오 계정)
    """
    delete_cookie("user")
    response = requests.get(f"{API_URL}/logout/account", allow_redirects=False)
    if response.status_code == 307:
        redirected_url = response.headers['Location']
        redirect(redirected_url)