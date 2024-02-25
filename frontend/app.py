import streamlit as st

from utils import (
    get_auth_url, redirect, get_userinfo,
    logout_cookie, logout_expire, logout_account,
    get_cookie
)

from config import BASE_URL


# 초기화
userid = get_cookie("userid")
code = st.query_params.get('code')

# UI 시작
st.title("FastAPI Kakao OIDC App")
st.subheader("FastAPI를 이용한 카카오 OIDC 인증 예제입니다.")
st.divider()

if not userid:
    if not code:
        # 로그인 페이지 (쿠키 정보 X / auth 코드 X)
        if st.button("카카오 로그인"):
            auth_url = get_auth_url()
            if auth_url:
                redirect(auth_url)
    else:
        # Redirect 및 사용자 정보 획득 (쿠키 정보 X / auth 코드 O)
        get_userinfo(code)
        redirect(BASE_URL)

else:
    # 메인 코드 (쿠키 정보 O)
    st.subheader("인증 정보")
    
    userid = get_cookie("userid")
    nickname = get_cookie("nickname")
    picture = get_cookie("picture")
    
    st.write({
        "userid": userid,
        "nickname": nickname,
        "picture": picture
    })

    c1, c2, c3 = st.columns(3)
    if c1.button("로그아웃 (쿠키 삭제)"):
        logout_cookie()
        redirect(BASE_URL)

    if c2.button("로그아웃 (토큰 만료)"):
        logout_expire()
        redirect(BASE_URL)

    if c3.button("로그아웃 (카카오 계정)"):
        logout_account()