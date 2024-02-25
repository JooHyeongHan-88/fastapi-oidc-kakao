from fastapi import FastAPI, Response, Header
from fastapi.middleware.cors import CORSMiddleware

import urllib.parse

from api.config import CLIENT_ID, REDIRECT_URI, AUTH_SERVER
from api.controller import OIDC, expire_token
from api.schema import AuthCode


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth")
async def return_userinfo(data: AuthCode):
    """
    1. auth code 이용한 토큰 및 사용자 정보 획득
    2. 사용자 정보 DB upsert
    3. Access Token 헤더에, 사용자 정보 쿠키에 담아 응답
    """
    oidc = OIDC(data.code)

    if oidc.get_auth() and oidc.set_userinfo():
        headers = {
            "Cache-Control": "no-cache",
            "Access-Token": oidc.access_token
        }

        response = Response(headers=headers)

        response.set_cookie("userid", urllib.parse.quote(oidc.userid))
        response.set_cookie("nickname", urllib.parse.quote(oidc.nickname))
        response.set_cookie("picture", urllib.parse.quote(oidc.picture))

        return response   


@app.get("/auth/redirect")
async def auth_url_api():
    """
    Kakao Auth URL로 리다이렉션
    """
    return Response(
        status_code=307,
        headers={"Location": f"{AUTH_SERVER}/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"}
    )


@app.get("/logout/token")
async def token_expire(access_token: str = Header(None)):
    """
    Kakao Auth Token 만료
    """
    if expire_token(access_token):
        return True
    

@app.get("/logout/account")
async def logout():
    """
    Kakao 계정 로그아웃
    """
    return Response(
        status_code=307,
        headers={"Location": f"{AUTH_SERVER}/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={REDIRECT_URI}"}
    )