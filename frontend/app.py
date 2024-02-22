import streamlit as st
import ast

from utils import get_auth_url, redirect, get_id_token, set_cookie, get_cookie
from config import BASE_URL


code = st.query_params.get('code')
user = get_cookie("user")

st.title("FastAPI Kakao OIDC App")
st.subheader("FastAPI를 이용한 Kakao OIDC 로그인 예제입니다.")
st.divider()


if not user:
    if not code:
        if st.button("카카오 로그인"):
            auth_url = get_auth_url()
            if auth_url:
                redirect(auth_url)
    else:
        res = get_id_token(code)
        st.session_state['user'] = res.json()
        set_cookie("user", res.json())
        redirect(BASE_URL)

else:
    user_dict = ast.literal_eval(user)
    st.write(user_dict)