import streamlit as st

from utils import (
    get_auth_url, redirect, get_userinfo,
    set_cookie, get_cookie,
    logout_cookie, logout_expire, logout_account
)

from config import BASE_URL


# 초기화
is_login = get_cookie("is_login")
code = st.query_params.get('code')

# UI 시작
st.title("FastAPI Kakao OIDC App")
st.subheader("FastAPI를 이용한 카카오 OIDC 인증 예제입니다.")
st.divider()

if not is_login:
    if not code:
        # 로그인 페이지 (쿠키 정보 X / auth 코드 X)
        if st.button("카카오 로그인"):
            auth_url = get_auth_url()
            if auth_url:
                redirect(auth_url)
    else:
        # Redirect 및 사용자 정보 획득 (쿠키 정보 X / auth 코드 O)
        userinfo = get_userinfo(code)
        if userinfo:
            set_cookie("is_login", "true")
            set_cookie("access_token", userinfo["access_token"])
            set_cookie("userid", userinfo["userid"])
            set_cookie("nickname", userinfo["nickname"])
            set_cookie("picture", userinfo["picture"])
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
        access_token = get_cookie("access_token")
        logout_expire(access_token)
        redirect(BASE_URL)

    if c3.button("로그아웃 (카카오 계정)"):
        logout_account()