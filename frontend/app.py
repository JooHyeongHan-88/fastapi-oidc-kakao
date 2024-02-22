import streamlit as st
import ast

from utils import get_auth_url, redirect, get_userinfo, set_cookie, get_cookie, logout_cookie, logout_expire, logout_account
from config import BASE_URL


user = get_cookie("user")
code = st.query_params.get('code')


st.title("FastAPI Kakao OIDC App")
st.subheader("FastAPI를 이용한 카카오 OIDC 인증 예제입니다.")
st.divider()

if not user:
    if not code:
        # 쿠키 정보 X / auth 코드 X
        if st.button("카카오 로그인"):
            auth_url = get_auth_url()
            if auth_url:
                redirect(auth_url)
    else:
        # 쿠키 정보 X / auth 코드 O
        userinfo = get_userinfo(code)
        if userinfo:
            set_cookie("user", userinfo)
        redirect(BASE_URL)

else:
    # 쿠키 정보 O
    st.subheader("인증 정보")
    user_dict = ast.literal_eval(user)
    st.write(user_dict)

    c1, c2, c3 = st.columns(3)
    if c1.button("로그아웃 (쿠키 삭제)"):
        logout_cookie()
        redirect(BASE_URL)
    if c2.button("로그아웃 (토큰 만료)"):
        logout_expire()
        redirect(BASE_URL)
    if c3.button("로그아웃 (카카오 계정)"):
        logout_account()