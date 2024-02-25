# FastAPI-OIDC-Kakao
FastAPI를 이용한 Kakao OIDC 로그인 예제.
> API 서버가 `access token`는 헤더로 `사용자 정보`는 쿠키로 응답하면 이를 브라우저(쿠키)에 저장한다.


## 사전 설정

### 1. 카카오 등록
[Kakao Developers](https://developers.kakao.com/)에서 어플리케이션 등록 ([카카오 소셜 로그인 구현](https://blog.naver.com/shino1025/222226561870) 참조).

> * `앱 설정 > 플랫폼 > Web > 사이트 도메인`에 `FastAPI` 호스팅 URL(http://127.0.0.1:8000) 입력.
> * `제품설정 > 카카오 로그인`에 `활성화 설정` 및 `OpenID Connect 활성화 설정` 상태를 `ON`으로 설정.
> * `제품설정 > 카카오 로그인` 내 `Redirect URI`에 `streamlit` 호스팅 URL(http://127.0.0.1:8501) 입력.
> * `제품설정 > 카카오 로그인 > 동의항목`에 `닉네임` 및 `프로필 사진` 항목을 `필수 동의`로 설정.
> * `제품설정 > 보안`에 `코드` 발급 받고 `활성화 상태`를 `사용함`으로 설정.
> * `제품설정 > 고급`에 `Logout Redirect URI`에 `streamlit` 호스팅 URL(http://127.0.0.1:8501) 입력.

### 2. 환경 설정

#### 환경 변수
API 서버 코드 내 `config.py` 파일 생성하여 카카오로부터 발급받은 `REST API Key`, `Client Secret`, `Redirect URI`를 다음과 같이 입력.

> **`config.py` 위치는 `./api/main.py`와 같은 위치에 생성한다.**

```python
# config.py 예시
AUTH_SERVER = "https://kauth.kakao.com"
API_SERVER = "https://kapi.kakao.com"

CLIENT_ID = "198f75998f7dc4f1198f75970400f56" # (REST API Key)
CLIENT_SECRET = "3pdc4f1198f759Ey4yFPR24198f759ZzO" # (Client Secret)
REDIRECT_URI = "http://localhost:8501" # (Redirect URI)
```

#### 가상 환경 + 패키지
`setup.bat` 파일 실행.

## 실행

아래 Front/Backend 서버 실행 후 `streamlit` 앱 (http://localhost:8501) 접속.

### 1. FastAPI 실행
터미널 프로젝트 디렉토리에서 아래 실행:
```shell
$ ./.venv/Scripts/activate # (가상환경 비활성 상태일 때)
$ uvicorn api.main:app --reload

...
INFO:     Will watch for changes in these directories: ['{프로젝트 디렉토리}']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using WatchFiles
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
...
```

### 2. Stremlit 실행
터미널 프로젝트 디렉토리에서 아래 실행:
```shell
$ ./.venv/Scripts/activate # (가상환경 비활성 상태일 때)
$ streamlit run frontend/app.py

...
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://XXX.XXX.XX.XXX:8501
...
```