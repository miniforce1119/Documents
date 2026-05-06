# 프로젝트 4: AI를 활용한 텔레그램 봇 만들기

> **유형**: 바이브 코딩 | **난이도**: :material-star::material-star::material-star: | **준비물**: Python, Git, VS Code, 텔레그램 앱

---

## 목표

AI에게 프롬프트로 코드를 요청해서, Google Sheets 기반의 **점심 메뉴 투표 텔레그램 봇**을 만듭니다. 코드를 직접 작성하지 않습니다.

---

## 전체 흐름

```
Google Sheets (점심 메뉴 데이터)
        ↓ Python이 읽어옴
   텔레그램 봇이 알림 전송
        ↑ 슬래쉬 커맨드로 조회/투표
```

---

## 준비물

- Python 3.10 이상 설치
- 본인이 사용하는 AI 도구 (ChatGPT, Claude, Cursor, Copilot 등 아무거나)
- Google 계정
- 텔레그램 앱 (휴대폰에 설치)

---

## STEP 1. 텔레그램 봇 만들기

텔레그램에서 나만의 봇을 만들어 봅니다. 코딩이 아니라 **채팅**으로 만듭니다.

### 1-1. BotFather에게 봇 생성 요청

1. 텔레그램 앱을 열고 검색창에 **@BotFather** 를 검색합니다
2. BotFather와 대화를 시작합니다
3. 아래 메시지를 보냅니다:

```
/newbot
```

4. 봇 이름을 물어봅니다 → 아무 이름이나 입력 (예: `우리팀 점심봇`)
5. 봇 username을 물어봅니다 → **반드시 `bot`으로 끝나야 합니다** (예: `ourteam_lunch_bot`)
6. 성공하면 **토큰**을 줍니다 → 반드시 메모합니다

```
예시: 7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

!!! warning "토큰 보안"
    이 토큰은 비밀번호와 같습니다. 다른 사람에게 공유하지 마세요.

### 1-2. 내 Chat ID 확인하기

1. 텔레그램에서 방금 만든 봇을 검색해서 대화를 시작합니다
2. 봇에게 아무 메시지나 보냅니다 (예: `/start`)
3. 웹 브라우저에서 아래 주소를 엽니다 (YOUR_BOT_TOKEN을 본인 토큰으로 교체):

```
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

4. 결과에서 `"chat":{"id":숫자}` 부분의 **숫자**가 내 Chat ID입니다

!!! tip "결과가 비어있다면?"
    봇에게 메시지를 보낸 후 브라우저에서 다시 새로고침하세요.

---

## STEP 2. Google Cloud 설정

Python에서 Google Sheets를 읽으려면 **서비스 계정**이 필요합니다.

### 2-1. Google Cloud 프로젝트 만들기

1. [Google Cloud Console](https://console.cloud.google.com) 에 접속합니다
2. 상단 프로젝트 선택 → **새 프로젝트** → 이름: `lunch-bot` → **만들기**

### 2-2. API 활성화

1. 좌측 메뉴 → **API 및 서비스** → **라이브러리**
2. `Google Sheets API` 검색 → **사용**
3. `Google Drive API` 검색 → **사용**

### 2-3. 서비스 계정 만들기

1. 좌측 메뉴 → **API 및 서비스** → **사용자 인증 정보**
2. **+ 사용자 인증 정보 만들기** → **서비스 계정**
3. 이름: `lunch-bot` → **만들기 및 계속** → 역할: **편집자** → **완료**

### 2-4. JSON 키 파일 다운로드

1. 만든 서비스 계정 클릭 → **키** 탭
2. **키 추가** → **새 키 만들기** → **JSON** → **만들기**
3. 다운로드된 파일을 프로젝트 폴더에 넣고 `credentials.json`으로 이름 변경

!!! warning "보안 주의"
    이 파일도 비밀번호와 같습니다. GitHub 등에 절대 올리지 마세요.

### 2-5. 서비스 계정 이메일 확인

`credentials.json` 파일을 메모장으로 열면 `client_email` 항목이 있습니다. 이 이메일을 메모합니다.

---

## STEP 3. Google Sheets 데이터 준비

1. [Google Drive](https://drive.google.com) 에 접속
2. 제공된 `점심메뉴_투표.xlsx` 파일을 업로드
3. Google Sheets로 열기
4. 우측 상단 **공유** → 2-5에서 메모한 서비스 계정 이메일 입력 → **편집자** 권한 → **보내기**
5. URL에서 스프레드시트 ID를 메모합니다:

```
https://docs.google.com/spreadsheets/d/여기가_스프레드시트_ID/edit
```

---

## STEP 4. 바이브 코딩 시작

AI에게 프롬프트를 주고 코드를 생성합니다. 아래 프롬프트를 AI에 복사해서 붙여넣으세요.

### 미션 1: 환경 설정 파일 만들기

```
파이썬 프로젝트를 하나 만들려고 해.

아래 정보를 .env 파일에 저장하는 구조를 만들어줘:
- TELEGRAM_BOT_TOKEN: 텔레그램 봇 토큰
- TELEGRAM_CHAT_ID: 텔레그램 채팅 ID
- GOOGLE_SHEETS_ID: 구글 스프레드시트 ID
- GOOGLE_CREDENTIALS_FILE: credentials.json

.env.example 파일도 만들어줘.

필요한 패키지 목록을 requirements.txt로 만들어줘:
- gspread, oauth2client, python-telegram-bot, python-dotenv, APScheduler
```

AI가 만들어준 코드로 `.env` 파일을 만들고 본인 정보를 입력한 후:

```bash
pip install -r requirements.txt
```

### 미션 2: Google Sheets 데이터 읽기

```
Python으로 Google Sheets에서 데이터를 읽어오는 코드를 만들어줘.

조건:
- gspread와 oauth2client 사용
- .env에서 설정값 로딩
- "점심메뉴" 시트에서 전체 데이터 읽기
- 컬럼: 날짜, 메뉴, 카테고리, 제안자, 투표수, 확정여부
- 오늘 날짜 메뉴만 필터링하는 함수
- 특정 메뉴의 투표수를 1 올리는 함수
- 파일명: sheets_manager.py
```

**테스트:**

```bash
python sheets_manager.py
```

### 미션 3: 텔레그램으로 메시지 보내기

```
Python으로 텔레그램 봇이 메시지를 보내는 코드를 만들어줘.

조건:
- python-telegram-bot 라이브러리 사용
- .env에서 토큰, Chat ID 로딩
- 오늘의 점심 메뉴를 sheets_manager.py에서 가져와서
  이모지로 보기 좋게 포맷팅해서 전송
- 파일명: telegram_bot.py
```

**테스트:**

```bash
python telegram_bot.py
```

텔레그램에 메시지가 오면 성공!

### 미션 4: 슬래쉬 커맨드 추가

```
텔레그램 봇에 슬래쉬 커맨드를 추가해줘.

추가할 커맨드:
1. /today - 오늘의 점심 메뉴 현황
2. /vote 메뉴이름 - 특정 메뉴에 투표
3. /help - 사용 가능한 명령어 안내

조건:
- python-telegram-bot의 Application 사용
- polling 방식으로 계속 실행
- 파일명: bot_commands.py
```

**테스트:**

```bash
python bot_commands.py
```

텔레그램에서 `/help`, `/today`, `/vote 김치찌개` 를 보내보세요.

---

## 완성 체크리스트

- [ ] `.env` 파일에 모든 설정값이 들어있다
- [ ] `python sheets_manager.py` → Google Sheets 데이터가 출력된다
- [ ] `python telegram_bot.py` → 텔레그램에 메시지가 온다
- [ ] `/today` 명령어 → 오늘 메뉴가 표시된다
- [ ] `/vote 메뉴이름` → 투표가 반영된다

---

## 트러블슈팅

에러가 나면 **에러 메시지를 그대로 복사해서 AI에게 물어보세요.**

```
이 에러가 발생했어. 원인과 해결 방법을 알려줘:

(에러 메시지 전체를 붙여넣기)

내 환경: Windows, Python 3.x
사용 라이브러리: gspread, python-telegram-bot, APScheduler
```

| 증상 | 원인 | 해결 |
|------|------|------|
| `ModuleNotFoundError` | 패키지 미설치 | `pip install 패키지명` |
| `FileNotFoundError: credentials.json` | 경로 문제 | 같은 폴더에 있는지 확인 |
| Google Sheets 접근 에러 | 공유 안 됨 | 서비스 계정에 시트 공유 확인 |
| `Forbidden: bot was blocked` | 봇 대화 미시작 | 봇에게 `/start` 보내기 |
| `Unauthorized` | 토큰 오류 | `.env` 봇 토큰 확인 |

---

## 핵심 포인트

!!! success "이 프로젝트에서 배우는 것"
    - AI에게 **단계별로 구체적인 프롬프트**를 주면 동작하는 코드가 나온다
    - 에러가 나면 **에러 메시지를 AI에게 그대로 보여주면** 해결된다
    - 코드를 몰라도 **실제 동작하는 서비스**를 만들 수 있다
    - 프롬프트에 **조건과 맥락**을 줄수록 정확한 결과가 나온다

---

## 프로젝트 최종 구조

```
lunch-bot/
├── .env                  ← 내 설정값 (비공개)
├── .env.example          ← 설정값 예시
├── credentials.json      ← Google 인증 키 (비공개)
├── requirements.txt      ← 필요한 패키지 목록
├── sheets_manager.py     ← Google Sheets 읽기/쓰기
├── telegram_bot.py       ← 텔레그램 메시지 전송
└── bot_commands.py       ← 슬래쉬 커맨드
```
