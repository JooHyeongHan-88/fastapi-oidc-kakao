import requests
from typing import Optional

from streamlitextras.webutils import stxs_javascript
from streamlitextras.cookiemanager import get_cookie_manager

from config import API_URL


# JavaScript 활용
def redirect(url: str) -> None:
    """
    redirection 수행 JS 코드 실행 (by. streamlit-extras)
    """
    stxs_javascript(f"window.location.replace('{url}');")


def set_cookie(name, value) -> None:
    """
    쿠키 저장 JS 코드 실행 (by. streamlit-extras)
    """
    stxs_javascript(f"document.cookie = '{name}={value}; path=/'")


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


# API 요청
def get_auth_url() -> Optional[str]:
    """
    API 서버로부터 redirection URL 반환
    : API 서버에서 RedirectResponse를 주어서 일반적으로는
    : URL 반환 필요 없이 redirection 되지만 프론트엔드가 파이썬이라
    : 브라우저에서 URL 받아서 직접 redirection 필요
    """
    response = requests.get(f"{API_URL}/auth/redirect", allow_redirects=False)
    if response.status_code == 307:
        redirected_url = response.headers['Location']
        return redirected_url
    else:
        return None


def get_userinfo(code: str) -> Optional[bool]:
    """
    API 서버에 access token 및 userinfo 요청 후 쿠키에 저장
    : 
    """
    response = requests.post(url=f"{API_URL}/auth", json={"code": code})

    if response.status_code == 200:
        access_token = response.headers["Access-Token"]
        cookies: dict = response.cookies.get_dict()

        set_cookie("access_token", access_token)

        for key, value in cookies.items():
            set_cookie(key, value)

        return True


# 로그아웃
def _delete_auth_cookies() -> None:
    """
    인증 정보 관련 저장한 쿠키 모두 삭제
    """
    delete_cookie("access_token")
    delete_cookie("userid")
    delete_cookie("nickname")
    delete_cookie("picture")


def logout_cookie() -> Optional[bool]:
    """
    로그아웃 (쿠키 삭제)
    """
    _delete_auth_cookies()
    return True


def logout_expire(access_token: str) -> Optional[bool]:
    """
    로그아웃 (토큰 만료)
    """
    access_token = get_cookie("access_token")

    _delete_auth_cookies()

    headers = {
        "Cache-Control": "no-cache",
        "Access-Token": access_token
    }

    response = requests.get(url=f"{API_URL}/logout/token", headers=headers)

    if response.status_code == 200:
        return True
    

def logout_account() -> None:
    """
    로그아웃 (카카오 계정)
    """
    _delete_auth_cookies()

    response = requests.get(f"{API_URL}/logout/account", allow_redirects=False)
    
    if response.status_code == 307:
        redirected_url = response.headers['Location']
        redirect(redirected_url)