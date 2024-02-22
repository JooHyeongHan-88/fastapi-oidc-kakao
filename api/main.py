from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from api.config import CLIENT_ID, REDIRECT_URI, AUTH_SERVER
from api.controller import OIDC
from api.model import UserData
from api.schema import AuthCode


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oidc = OIDC()


@app.post("/auth")
async def return_userinfo(data: AuthCode):
    """
    1. auth code 획득
    2. auth code 이용한 클라이언트 인증 및 id_token 발급
    3. id_token 디코딩 및 userinfo 획득
    4. userinfo DB upsert 및 return
    """
    code = data.code

    if oidc.auth(code):
        userinfo = oidc.userinfo

        user = UserData(userinfo)
        # TODO: 유저 DB 등록

        return userinfo


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
async def token_expire():
    """
    Kakao Auth Token 만료
    """
    if oidc.expire_token():
        return True
    

@app.get("/logout/account")
async def logout_account():
    """
    Kakao 계정 로그아웃
    """
    return Response(
        status_code=307,
        headers={"Location": f"{AUTH_SERVER}/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={REDIRECT_URI}"}
    )