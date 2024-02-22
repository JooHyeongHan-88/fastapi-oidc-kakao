import json

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from api.config import CLIENT_ID, REDIRECT_URI
from api.controller import OIDC, decode64
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


@app.post("/auth")
async def post_userinfo(data: AuthCode):
    """
    1. auth code 획득
    2. auth code 이용한 인증 및 id_token 발급
    3. id_token 파싱 및 userinfo 획득
    4. userinfo DB upsert 및 return
    """
    code = data.code

    oidc = OIDC()
    token_info = oidc.auth(code)
    id_token = token_info['id_token']

    _, payload, _ = id_token.split(".")
    userinfo = decode64(payload)
    userinfo = json.loads(userinfo)

    user = UserData(userinfo)
    # TODO: 유저 DB 등록

    return userinfo


@app.get("/auth/url")
async def auth_url_api():
    """
    Kakao Auth URL로 리다이렉션
    """
    return Response(
        status_code=307,
        headers={"Location": f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code" }
    )