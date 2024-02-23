from fastapi import FastAPI, Response, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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
    3. userinfo DB upsert 및 return
    """
    oidc = OIDC(data.code)

    if oidc.get_auth() and oidc.set_userinfo():
        headers = {
            "Cache-Control": "no-cache",
            "Access-Token": oidc.access_token
        }
        contents = {
            "userid": oidc.userid,
            "nickname": oidc.nickname,
            "picture": oidc.picture
        }

        # 필요에 따라 유저 DB 등록

        return JSONResponse(content=contents, headers=headers)


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