# 🏢 회사 배포 빠른 시작 가이드

> **목적:** 이 문서화 시스템을 회사 GitHub Enterprise에 빠르게 배포하기 위한 가이드입니다.

---

## 📦 패키지 내용물

```
agent-builder-automation-package.tar.gz
│
├── docs/                           # 문서 폴더 (Markdown)
│   ├── courses/                    # 교육 자료
│   │   └── ai-fundamentals.md      # ✨ 새로 작성된 AI 입문 문서 (2시간 분량)
│   ├── guides/                     # 가이드 문서
│   ├── concepts/                   # 개념 설명 문서
│   ├── analysis/                   # 분석 문서
│   └── images/                     # 이미지 자료
│       └── ai-fundamentals/        # AI 입문 문서 이미지 (3개)
│
├── doc_review_app.py               # Streamlit 문서 관리 앱
├── mkdocs.yml                      # MkDocs 설정 파일
├── requirements.txt                # Python 패키지 목록
│
├── COMPANY_PORTING_GUIDE.md        # ⭐ 회사 포팅 상세 가이드
├── CLINE_TODO.md                   # ⭐ Cline 작업 체크리스트
├── TEST_GUIDE_2MODE.md             # Mode A/B 테스트 가이드
├── IMPLEMENTATION_SUMMARY.md       # 시스템 아키텍처
└── .gitignore                      # Git 제외 파일 목록
```

---

## 🚀 5분 빠른 시작

### Step 1: 압축 해제

```bash
# 회사 PC에서
cd /your/workspace/
tar -xzf agent-builder-automation-package.tar.gz
cd agent-builder-automation/
```

### Step 2: Python 가상환경 설정

```bash
# Python 3.10 이상 필요
python3 -m venv venv

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### Step 3: 환경 변수 설정

```bash
# .env 파일 생성
cat > .env << 'EOF'
# Agent Builder API (나중에 입력)
AGENT_REFORMAT_URL=https://your-company-agent-api.com/reformat
AGENT_API_KEY=your-api-key-here

# GitHub Enterprise
GITHUB_TOKEN=your-github-token-here
EOF

# 보안 설정
chmod 600 .env
```

### Step 4: Git 저장소 연결

```bash
# 새 저장소 생성하는 경우
git init
git remote add origin https://github.company.com/your-team/docs-automation.git

# 또는 기존 저장소 클론
git clone https://github.company.com/your-team/docs-automation.git
# 그 후 agent-builder-automation 폴더 내용을 복사
```

### Step 5: 첫 커밋 & 푸시

```bash
git add .
git commit -m "Initial commit: AI documentation automation system"
git push -u origin main
```

---

## 📚 새로 작성된 AI 입문 문서

### 문서 정보

**파일:** `docs/courses/ai-fundamentals.md`  
**제목:** AI 개요 및 주요 용어 설명  
**분량:** 약 10,000자 (2시간 학습 분량)  
**난이도:** ⭐ 입문  
**포함 이미지:** 3개

### 문서 구성

```
1. AI란 무엇인가? (30분)
   - AI의 정의
   - AI vs 일반 프로그램
   - 왜 지금 AI가 중요한가

2. AI의 종류와 발전 단계 (20분)
   - 약한/강한/초지능 AI
   - AI 발전 타임라인

3. 머신러닝 기초 (30분)
   - 지도/비지도/강화 학습
   - 핵심 요소

4. 딥러닝 이해하기 (20분)
   - 신경망 구조
   - CNN, RNN, Transformer

5. 주요 AI 용어 사전 (30분)
   - 50개 핵심 용어 설명
   - LLM, 프롬프트, RAG 등

6. 실생활 속 AI 사례 (15분)
   - 일상/산업별 활용

7. AI 활용 시 알아야 할 것들 (20분)
   - 한계, 윤리, 활용법

8. 다음 단계 (15분)
   - 학습 로드맵, 실습 가이드
```

### 특징

✅ 쉬운 설명 (비전공자 용어 없음)  
✅ 3개 이미지 포함  
✅ 실생활 사례 풍부  
✅ 체크리스트 & FAQ  
✅ 즉시 교육에 활용 가능

---

## 🎯 회사 Cline에게 요청할 내용

### 1단계: 기본 설정 (10분)

```
"agent-builder-automation-package.tar.gz 파일을 압축 해제하고,
Python venv를 생성한 후 requirements.txt를 설치해줘.

그리고 .env 파일을 생성하되,
AGENT_API_KEY는 비워두고 나중에 내가 입력할게."
```

### 2단계: Git 저장소 설정 (10분)

```
"회사 GitHub Enterprise 저장소를 생성하거나 클론해줘.
저장소 URL: https://github.company.com/your-team/docs-automation

그리고 현재 폴더를 Git 저장소로 초기화하고
첫 커밋을 만들어서 push해줘."
```

### 3단계: MkDocs 로컬 확인 (5분)

```
"MkDocs 로컬 서버를 실행해서 문서가 제대로 보이는지 확인해줘.

명령어: mkdocs serve

특히 docs/courses/ai-fundamentals.md 문서가
이미지 3개와 함께 잘 표시되는지 확인해줘."
```

### 4단계: GitHub Pages 설정 (15분)

```
"COMPANY_PORTING_GUIDE.md 파일의
'4. GitHub Pages 설정' 섹션을 참고해서

1. GitHub Enterprise에서 Pages를 활성화하고
2. mkdocs.yml 파일의 site_url과 repo_url을 회사 URL로 수정하고
3. mkdocs gh-deploy 명령으로 첫 배포를 해줘."
```

### 5단계: Agent Builder 연동 (나중에)

```
"CLINE_TODO.md 파일을 참고해서
doc_review_app.py의 reformat_external_text() 함수를
회사 Agent Builder API로 교체해줘.

자세한 내용은 CLINE_TODO.md를 참고."
```

---

## 📖 주요 문서 설명

### ⭐ COMPANY_PORTING_GUIDE.md (가장 중요!)

**내용:**
- Python venv 설정
- Git 저장소 연결
- Agent Builder API 연동
- GitHub Pages 배포
- 보안 & 트러블슈팅

**언제 보나:**
- 전체 시스템 이해할 때
- 문제 해결할 때
- 상세 설정 필요할 때

### ⭐ CLINE_TODO.md

**내용:**
- Agent Builder API 연동 상세 가이드
- 환경 변수 설정
- 테스트 방법
- 체크리스트

**언제 보나:**
- Agent API 연결할 때
- Mode B (외부 AI 재구성) 사용할 때

### 📘 TEST_GUIDE_2MODE.md

**내용:**
- Mode A (Agent Builder 직접) 테스트
- Mode B (외부 AI 재구성) 테스트
- 전체 워크플로우 검증

**언제 보나:**
- 시스템 테스트할 때
- 문제 확인할 때

### 📕 IMPLEMENTATION_SUMMARY.md

**내용:**
- 시스템 아키텍처
- 주요 컴포넌트
- 데이터 흐름

**언제 보나:**
- 시스템 구조 이해할 때
- 확장/수정할 때

---

## 🔧 필수 확인 사항

### Python 버전

```bash
python3 --version
# Python 3.10 이상 필요
```

### Git 설치

```bash
git --version
# git version 2.x.x
```

### GitHub Enterprise 접근 권한

```bash
# Personal Access Token 또는 SSH Key 필요
# Settings → Developer settings → Personal access tokens
```

### 회사 방화벽/프록시

```bash
# 프록시 설정이 필요한 경우 .env에 추가:
# HTTP_PROXY=http://proxy.company.com:8080
# HTTPS_PROXY=http://proxy.company.com:8080
```

---

## 📂 디렉토리 구조 이해

```
agent-builder-automation/
│
├── docs/                    # 📝 여기에 Markdown 문서 작성
│   ├── courses/             # 교육 자료
│   ├── guides/              # 가이드
│   ├── concepts/            # 개념 설명
│   ├── analysis/            # 분석 문서
│   └── images/              # 이미지 자료
│
├── inbox/                   # 📥 임시 저장 (자동 생성)
├── published/               # 📤 발행 완료 (자동 생성)
│
├── doc_review_app.py        # 🖥️ Streamlit 앱
├── mkdocs.yml               # ⚙️ MkDocs 설정
├── requirements.txt         # 📦 Python 패키지
│
├── .env                     # 🔐 환경 변수 (직접 생성)
├── .gitignore               # 🚫 Git 제외 목록
│
└── [가이드 문서들]          # 📚 포팅/사용 가이드
```

---

## 🎓 새 문서 작성 방법

### 방법 1: 직접 Markdown 작성

```bash
# 적절한 카테고리 폴더에 파일 생성
touch docs/courses/your-new-course.md

# 내용 작성 후
git add docs/courses/your-new-course.md
git commit -m "docs: add new course"
git push

# 배포
mkdocs gh-deploy --force
```

### 방법 2: Streamlit 앱 사용

```bash
# Streamlit 앱 실행
streamlit run doc_review_app.py

# 브라우저에서:
# 1. Mode A 또는 Mode B 선택
# 2. 내용 입력/변환
# 3. Preview → Inbox → Publish
# (자동으로 Git push & MkDocs deploy)
```

---

## ⚡ 자주 사용하는 명령어

### 로컬 개발

```bash
# 가상환경 활성화
source venv/bin/activate

# MkDocs 로컬 서버
mkdocs serve
# → http://localhost:8000

# Streamlit 앱 실행
streamlit run doc_review_app.py
# → http://localhost:8501
```

### Git 작업

```bash
# 상태 확인
git status

# 변경 사항 커밋
git add .
git commit -m "docs: update documentation"
git push

# 원격 최신 가져오기
git pull origin main
```

### 배포

```bash
# GitHub Pages 배포
mkdocs gh-deploy --force --clean

# 배포 확인
# https://your-team.github.company.com/docs-automation/
```

---

## 🐛 문제 해결

### venv 생성 실패

```bash
# Python 버전 확인
python3 --version

# pip 업그레이드
python3 -m pip install --upgrade pip

# 다시 시도
python3 -m venv venv
```

### Git push 실패

```bash
# 인증 확인
git remote -v

# Token 재설정
git remote set-url origin https://YOUR_TOKEN@github.company.com/team/repo.git
```

### MkDocs 빌드 오류

```bash
# 캐시 삭제
rm -rf site/

# 다시 빌드
mkdocs build --clean
```

### 프록시 오류

```bash
# .env에 추가
echo "HTTP_PROXY=http://proxy.company.com:8080" >> .env
echo "HTTPS_PROXY=http://proxy.company.com:8080" >> .env
```

---

## 📞 추가 도움말

### 상세 가이드

- **전체 포팅:** `COMPANY_PORTING_GUIDE.md`
- **Agent 연동:** `CLINE_TODO.md`
- **테스트:** `TEST_GUIDE_2MODE.md`
- **아키텍처:** `IMPLEMENTATION_SUMMARY.md`

### 문서 작성 요청

새 문서가 필요하면 주제와 요구사항을 알려주세요:
- 대상 독자 (초급/중급/고급)
- 포함할 내용
- 문서 형태 (Markdown/HTML)
- 카테고리 (courses/guides/concepts/analysis)

---

## ✅ 배포 완료 체크리스트

```
환경 설정:
[ ] Python venv 생성 완료
[ ] requirements.txt 설치 완료
[ ] .env 파일 생성 완료

Git:
[ ] 저장소 생성/클론 완료
[ ] 첫 커밋 & push 성공

MkDocs:
[ ] mkdocs serve로 로컬 확인 완료
[ ] AI 입문 문서가 잘 보임 (이미지 포함)

GitHub Pages:
[ ] Pages 활성화 완료
[ ] mkdocs gh-deploy 성공
[ ] 웹사이트 접속 가능

문서 확인:
[ ] AI 입문 문서 (ai-fundamentals.md) 확인
[ ] 이미지 3개 정상 표시
[ ] 네비게이션 동작 확인
```

---

## 🎉 시작하기

**1. 압축 해제:**
```bash
tar -xzf agent-builder-automation-package.tar.gz
cd agent-builder-automation/
```

**2. Cline에게 요청:**
```
"COMPANY_DEPLOYMENT_QUICKSTART.md를 참고해서
이 문서화 시스템을 회사 GitHub Enterprise에 배포해줘.

1단계부터 4단계까지 순서대로 진행하고,
각 단계가 완료되면 결과를 알려줘."
```

**3. 배포 확인:**
```
https://your-team.github.company.com/docs-automation/courses/ai-fundamentals/
```

---

**작성일:** 2026-03-11  
**버전:** 1.0  
**대상:** 회사 Cline & 개발팀  
**상태:** ✅ 즉시 사용 가능
