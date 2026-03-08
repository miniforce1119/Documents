# 🏢 회사 포팅 가이드 (Company Porting Guide)

> **목적:** 이 문서 시스템을 회사 환경으로 포팅할 때 필요한 모든 사항을 정리한 가이드입니다.

---

## 📋 목차

1. [환경 설정](#1-환경-설정)
2. [Git 저장소 설정](#2-git-저장소-설정)
3. [Agent Builder 연동](#3-agent-builder-연동)
4. [GitHub Pages 설정](#4-github-pages-설정)
5. [주의사항 및 보안](#5-주의사항-및-보안)
6. [트러블슈팅](#6-트러블슈팅)
7. [Cline 작업 체크리스트](#7-cline-작업-체크리스트)

---

## 1. 환경 설정

### 1.1 Python 가상환경 (venv) 설정

```bash
# 회사 프로젝트 디렉토리로 이동
cd /path/to/your-company-docs-project

# venv 생성
python3 -m venv venv

# venv 활성화
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 활성화 확인 (프롬프트에 (venv) 표시됨)
which python  # macOS/Linux
where python  # Windows
```

### 1.2 필수 패키지 설치

현재 디렉토리의 `requirements.txt` 확인:

```bash
cat requirements.txt
```

예상 내용:
```
streamlit>=1.28.0
mkdocs>=1.5.0
mkdocs-material>=9.4.0
python-dotenv>=1.0.0
requests>=2.31.0
```

설치:
```bash
pip install -r requirements.txt
```

### 1.3 .gitignore 확인

**중요:** 회사 환경에서 민감 정보가 Git에 포함되지 않도록:

```bash
cat .gitignore
```

필수 항목:
```gitignore
# Virtual Environment
venv/
env/
.venv/

# Environment Variables (중요!)
.env
.env.local
.env.production

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/

# MkDocs
site/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Streamlit
.streamlit/secrets.toml

# Inbox & Published (선택적)
inbox/
published/
```

---

## 2. Git 저장소 설정

### 2.1 회사 Git 저장소 연결

#### **Case A: 새 저장소 생성**

```bash
# 현재 프로젝트를 Git 저장소로 초기화
git init

# 회사 GitHub Enterprise 또는 GitLab에 remote 추가
git remote add origin https://github.company.com/your-team/docs-automation.git

# 또는 GitLab:
# git remote add origin https://gitlab.company.com/your-team/docs-automation.git

# 첫 커밋
git add .
git commit -m "Initial commit: documentation automation system"

# Push
git push -u origin main
```

#### **Case B: 기존 저장소 사용**

```bash
# 회사 저장소 클론
git clone https://github.company.com/your-team/docs-automation.git
cd docs-automation

# 현재 코드를 복사 (agent-builder-automation 폴더 전체)
# 그리고 Git add/commit/push
```

### 2.2 Git 인증 설정

#### **Option 1: Personal Access Token (추천)**

```bash
# GitHub Enterprise에서 Personal Access Token 생성
# Settings → Developer settings → Personal access tokens → Generate new token

# 권한 선택:
# - repo (전체 접근)
# - workflow (GitHub Actions 사용 시)

# Git remote URL에 토큰 포함
git remote set-url origin https://YOUR_TOKEN@github.company.com/your-team/docs-automation.git
```

#### **Option 2: SSH Key**

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your.email@company.com"

# 공개 키 복사
cat ~/.ssh/id_ed25519.pub

# GitHub Enterprise/GitLab에 등록
# Settings → SSH Keys → Add SSH Key

# Git remote를 SSH로 변경
git remote set-url origin git@github.company.com:your-team/docs-automation.git
```

### 2.3 Branch 전략

```bash
# Main 브랜치: 안정 버전
git checkout -b main

# 개발 브랜치: 신규 기능
git checkout -b develop

# 기능별 브랜치
git checkout -b feature/agent-integration
git checkout -b feature/custom-template
```

---

## 3. Agent Builder 연동

### 3.1 환경 변수 설정

회사 디렉토리에 `.env` 파일 생성:

```bash
cd /path/to/your-company-docs-project
cat > .env << 'EOF'
# Agent Builder API Configuration
AGENT_REFORMAT_URL=https://agent-builder.company.com/api/reformat
AGENT_API_KEY=your-actual-api-key-here

# GitHub Configuration (선택적)
GITHUB_TOKEN=your-github-token-here
GITHUB_REPO=your-team/docs-automation

# MkDocs Configuration (선택적)
MKDOCS_SITE_NAME=Company Documentation
MKDOCS_SITE_URL=https://docs.company.com
EOF

# 파일 권한 설정 (보안)
chmod 600 .env
```

### 3.2 API 스펙 확인

**Cline에게 요청할 질문:**

```
1. "회사 Agent Builder의 Reformat API 엔드포인트 URL은?"
2. "API 인증 방식은? (Bearer Token / API Key / OAuth)"
3. "요청 포맷은? (JSON body 예시)"
4. "응답 포맷은? (예시 JSON)"
5. "에러 코드는? (401, 429 등)"
6. "Rate Limit은? (시간당 호출 제한)"
```

### 3.3 코드 수정 위치

**파일:** `doc_review_app.py`

**수정 함수:** `reformat_external_text()` (약 60번째 줄)

**현재 (Mock):**
```python
def reformat_external_text(text: str) -> tuple[str, str, str]:
    # Mock implementation
    lines = text.strip().split('\n')
    title = lines[0][:50] if lines else "Untitled"
    # ...
```

**변경 후 (실제 API):**
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def reformat_external_text(text: str) -> tuple[str, str, str]:
    """회사 Reformat Agent API 호출"""
    url = os.getenv("AGENT_REFORMAT_URL")
    api_key = os.getenv("AGENT_API_KEY")
    
    if not api_key:
        raise ValueError("AGENT_API_KEY 환경 변수가 없습니다.")
    
    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={"input": text, "output_format": "markdown_document"},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        return (
            result["title"],
            result.get("filename", sanitize_filename(result["title"])),
            result["content"]
        )
    except Exception as e:
        raise RuntimeError(f"Reformat Agent 호출 실패: {e}")
```

### 3.4 테스트 스크립트

API 연결 테스트용:

```bash
cat > test_reformat_api.py << 'EOF'
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_api():
    url = os.getenv("AGENT_REFORMAT_URL")
    key = os.getenv("AGENT_API_KEY")
    
    test_text = """
    Python 성능 최적화 팁
    
    1. 리스트 컴프리헨션 사용
    2. 제너레이터 활용
    3. 내장 함수 우선
    """
    
    print(f"📡 API URL: {url}")
    print(f"🔑 API Key: {key[:10]}..." if key else "❌ No API Key")
    
    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}"},
            json={"input": test_text},
            timeout=10
        )
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
EOF

# 실행
python test_reformat_api.py
```

---

## 4. GitHub Pages 설정

### 4.1 회사 GitHub Enterprise에서 Pages 활성화

#### **Step 1: Repository 설정**

1. GitHub Enterprise에서 저장소로 이동
2. `Settings` → `Pages`
3. Source: `Deploy from a branch`
4. Branch: `gh-pages` 선택, `/root` 선택
5. `Save` 클릭

#### **Step 2: GitHub Actions 권한 설정**

1. `Settings` → `Actions` → `General`
2. `Workflow permissions`:
   - ✅ `Read and write permissions` 선택
   - ✅ `Allow GitHub Actions to create and approve pull requests` 체크
3. `Save` 클릭

### 4.2 GitHub Actions Workflow 수정

**중요:** 회사 GitHub Enterprise URL에 맞게 수정 필요

현재 `.github/workflows/deploy-docs.yml` 확인:

```bash
cat .github/workflows/deploy-docs.yml
```

**회사 환경에 맞게 수정:**

```yaml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - '.github/workflows/deploy-docs.yml'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install mkdocs mkdocs-material

      - name: Configure git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Deploy to GitHub Pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          mkdocs gh-deploy --force --clean --verbose
```

**주의사항:**
- `uses: actions/checkout@v4` 등의 Actions가 회사 GitHub Enterprise에서 사용 가능한지 확인
- 불가능하면 Marketplace에서 대체 Action 찾기 또는 직접 스크립트 작성

### 4.3 MkDocs 설정 수정

`mkdocs.yml` 파일에서 회사 URL 변경:

```yaml
site_name: "Company Documentation System"
site_description: "회사 AI 문서 자동화 시스템"
site_author: "Your Team Name"
site_url: https://your-team.github.company.com/docs-automation/  # 회사 URL
repo_url: https://github.company.com/your-team/docs-automation
repo_name: your-team/docs-automation
edit_uri: edit/main/docs/

theme:
  name: material
  language: ko
  # ... 나머지 설정
```

### 4.4 수동 배포 (GitHub Actions 없이)

회사에서 GitHub Actions가 제한되어 있다면:

```bash
# 가상환경 활성화
source venv/bin/activate

# MkDocs 빌드 & 배포
cd /path/to/your-company-docs-project
mkdocs gh-deploy --force --clean

# 결과 확인
# https://your-team.github.company.com/docs-automation/
```

**Streamlit 앱에서 자동 배포 유지:**
- `doc_review_app.py`의 `git_commit_and_push()` 함수가 이미 `mkdocs gh-deploy`를 호출
- Publish 버튼 클릭 시 자동으로 GitHub Pages 업데이트 ✅

---

## 5. 주의사항 및 보안

### 5.1 민감 정보 관리

#### **절대 Git에 포함하면 안 되는 것:**

```
❌ .env 파일
❌ API Keys
❌ GitHub Personal Access Tokens
❌ 회사 내부 URL (공개 저장소일 경우)
❌ 비밀번호
```

#### **.env 파일 보안:**

```bash
# 파일 권한 설정
chmod 600 .env

# .gitignore에 포함 확인
echo ".env" >> .gitignore

# Git history에서 제거 (실수로 커밋한 경우)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all
```

### 5.2 Streamlit Secrets 관리

**Option 1: .env 파일 (로컬 개발)**

```bash
# .env
AGENT_API_KEY=abc123
```

**Option 2: Streamlit Secrets (배포 시)**

```bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
AGENT_API_KEY = "abc123"
AGENT_REFORMAT_URL = "https://agent-builder.company.com/api/reformat"
EOF

# .gitignore에 추가
echo ".streamlit/secrets.toml" >> .gitignore
```

코드에서 사용:
```python
import streamlit as st
import os

# 로컬: .env에서, 배포: secrets.toml에서
api_key = st.secrets.get("AGENT_API_KEY", os.getenv("AGENT_API_KEY"))
```

### 5.3 회사 방화벽 & 프록시

회사 네트워크에서 외부 API 호출 시:

```python
# doc_review_app.py 수정
import os

# 회사 프록시 설정
proxies = None
if os.getenv("HTTP_PROXY"):
    proxies = {
        "http": os.getenv("HTTP_PROXY"),
        "https": os.getenv("HTTPS_PROXY", os.getenv("HTTP_PROXY"))
    }

# API 호출 시 프록시 사용
response = requests.post(
    url,
    headers={"Authorization": f"Bearer {api_key}"},
    json={"input": text},
    proxies=proxies,  # 추가
    timeout=30
)
```

`.env`에 프록시 추가:
```bash
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
```

---

## 6. 트러블슈팅

### 6.1 Git Push 실패

#### **문제:** `error: failed to push some refs`

**원인 1:** 인증 실패

```bash
# Personal Access Token 재발급 후
git remote set-url origin https://NEW_TOKEN@github.company.com/your-team/docs-automation.git
```

**원인 2:** Branch 보호 규칙

```bash
# Pull request를 통해서만 merge 가능한 경우
git checkout -b feature/update-docs
git push -u origin feature/update-docs
# 그 후 웹에서 Pull Request 생성
```

**원인 3:** 대용량 파일

```bash
# Git LFS 설치 & 사용
git lfs install
git lfs track "*.pdf"
git add .gitattributes
git commit -m "Add Git LFS for large files"
```

### 6.2 MkDocs 빌드 실패

#### **문제:** `ERROR - Config value: 'theme'. Error: Unrecognised theme name: 'material'`

```bash
# material 테마 설치
pip install mkdocs-material

# 또는 requirements.txt 재설치
pip install -r requirements.txt
```

#### **문제:** `WARNING - A 'site_url' is not set`

```bash
# mkdocs.yml에 추가
site_url: https://your-team.github.company.com/docs-automation/
```

### 6.3 Streamlit 앱 실행 오류

#### **문제:** `ModuleNotFoundError: No module named 'streamlit'`

```bash
# venv 활성화 확인
source venv/bin/activate

# 패키지 재설치
pip install -r requirements.txt
```

#### **문제:** `FileNotFoundError: [Errno 2] No such file or directory: 'docs'`

```bash
# docs 폴더 생성
mkdir -p docs/analysis docs/guides docs/reports docs/concepts
touch docs/index.md
```

### 6.4 Agent API 호출 실패

#### **문제:** `401 Unauthorized`

```bash
# .env 파일 확인
cat .env | grep AGENT_API_KEY

# API 키 재발급 후 업데이트
```

#### **문제:** `timeout after 30 seconds`

```python
# doc_review_app.py에서 timeout 증가
response = requests.post(..., timeout=60)  # 30 → 60초
```

#### **문제:** `SSL Certificate Verification Failed`

```python
# 회사 자체 인증서 사용 시 (임시 해결책)
response = requests.post(..., verify=False)

# 또는 회사 CA 인증서 지정
response = requests.post(..., verify='/path/to/company-ca.crt')
```

---

## 7. Cline 작업 체크리스트

### 7.1 초기 설정 (Phase 1)

```
회사 Cline에게 요청할 것:

[ ] "Python venv를 생성하고 requirements.txt를 설치해줘"
[ ] "회사 GitHub Enterprise 저장소를 생성하거나 클론해줘"
[ ] ".gitignore 파일에 .env와 venv/가 포함되어 있는지 확인해줘"
[ ] ".env 파일을 생성하고 AGENT_API_KEY 변수를 추가해줘 (값은 나중에 수동 입력)"
```

### 7.2 Agent Builder 연동 (Phase 2)

```
[ ] "회사 Agent Builder API 문서를 찾아줘"
[ ] "API 엔드포인트 URL과 인증 방식을 알려줘"
[ ] "doc_review_app.py의 reformat_external_text() 함수를 회사 API로 교체해줘"
[ ] "test_reformat_api.py 스크립트로 API 연결을 테스트해줘"
[ ] "에러 처리와 Fallback 로직을 추가해줘"
```

### 7.3 GitHub Pages 설정 (Phase 3)

```
[ ] "회사 GitHub Enterprise에서 Pages 설정 방법을 알려줘"
[ ] "mkdocs.yml 파일의 site_url과 repo_url을 회사 URL로 수정해줘"
[ ] ".github/workflows/deploy-docs.yml이 회사 환경에서 작동하는지 확인해줘"
[ ] "Streamlit에서 Publish 버튼 클릭 시 자동 배포가 되는지 테스트해줘"
```

### 7.4 보안 & 최적화 (Phase 4)

```
[ ] ".env 파일이 절대 Git에 포함되지 않도록 확인해줘"
[ ] "회사 프록시 설정이 필요한지 확인하고 추가해줘"
[ ] "API 타임아웃과 Rate Limit 처리를 추가해줘"
[ ] "로그에 민감 정보(API 키)가 노출되지 않도록 마스킹해줘"
```

### 7.5 테스트 & 검증 (Phase 5)

```
[ ] "Mode A (Agent Builder 직접)를 테스트해줘"
[ ] "Mode B (외부 AI → Reformat)를 테스트해줘"
[ ] "긴 텍스트(1000줄 이상)로 테스트해줘"
[ ] "에러 케이스를 테스트해줘 (잘못된 API 키, 네트워크 오류 등)"
[ ] "최종 워크플로우를 전체 실행해줘: Save → Review → Publish → GitHub Pages 확인"
```

---

## 8. 빠른 시작 명령어 모음

### 8.1 로컬 개발

```bash
# 1. 가상환경 생성 & 활성화
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 2. 패키지 설치
pip install -r requirements.txt

# 3. .env 파일 생성 (수동으로 API 키 입력)
cat > .env << 'EOF'
AGENT_REFORMAT_URL=https://agent-builder.company.com/api/reformat
AGENT_API_KEY=your-api-key-here
EOF

# 4. Streamlit 앱 실행
streamlit run doc_review_app.py

# 5. MkDocs 로컬 서버 (선택적)
mkdocs serve
```

### 8.2 배포

```bash
# Git 커밋 & 푸시
git add .
git commit -m "Update documentation"
git push origin main

# GitHub Pages 수동 배포 (필요 시)
mkdocs gh-deploy --force --clean
```

### 8.3 문제 해결

```bash
# venv 재생성
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Git 원격 재설정
git remote -v
git remote set-url origin https://NEW_TOKEN@github.company.com/your-team/docs-automation.git

# MkDocs 캐시 삭제
rm -rf site/
mkdocs build --clean
```

---

## 9. 참고 문서

### 내부 문서

1. **CLINE_TODO.md** - Cline 작업 상세 가이드
2. **TEST_GUIDE_2MODE.md** - Mode A/B 테스트 가이드
3. **IMPLEMENTATION_SUMMARY.md** - 시스템 아키텍처 문서
4. **GITHUB_ACTIONS_SETUP.md** - GitHub Actions 설정 가이드

### 외부 참고

- [MkDocs 공식 문서](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Streamlit 문서](https://docs.streamlit.io/)
- [Python venv 가이드](https://docs.python.org/3/library/venv.html)
- [GitHub Enterprise 문서](https://docs.github.com/en/enterprise-cloud@latest)

---

## 10. 최종 체크리스트

### ✅ 포팅 완료 기준

```
환경 설정:
[ ] Python venv 생성 완료
[ ] requirements.txt 설치 완료
[ ] .env 파일 생성 및 API 키 설정 완료
[ ] .gitignore 확인 완료

Git 설정:
[ ] 회사 저장소 생성/클론 완료
[ ] Git remote 설정 완료
[ ] 인증 설정 완료 (Token 또는 SSH)
[ ] 첫 커밋 & 푸시 성공

Agent Builder:
[ ] API 스펙 확인 완료
[ ] reformat_external_text() 함수 교체 완료
[ ] API 연결 테스트 성공
[ ] 에러 처리 추가 완료

GitHub Pages:
[ ] Pages 활성화 완료
[ ] mkdocs.yml 회사 URL 수정 완료
[ ] GitHub Actions 설정 완료 (또는 수동 배포 확인)
[ ] 배포 테스트 성공

보안:
[ ] .env 파일이 Git에 포함되지 않음 확인
[ ] API 키가 코드에 하드코딩되지 않음 확인
[ ] 로그에 민감 정보 노출 없음 확인

기능 테스트:
[ ] Mode A (Agent Builder) 정상 작동
[ ] Mode B (외부 AI → Reformat) 정상 작동
[ ] Preview → Inbox → Publish 흐름 정상
[ ] GitHub Pages 자동 배포 정상
[ ] MkDocs 사이트 정상 표시

문서화:
[ ] 팀원에게 사용법 공유
[ ] API 키 관리 방법 공유
[ ] 트러블슈팅 가이드 공유
```

---

## 📞 Cline에게 전달할 한 줄 요약

```
"이 문서 자동화 시스템을 회사 환경에 포팅하려고 합니다. 
Python venv 설정, 회사 GitHub Enterprise 연결, Agent Builder API 연동, 
그리고 GitHub Pages 배포를 도와주세요. 
자세한 내용은 COMPANY_PORTING_GUIDE.md와 CLINE_TODO.md를 참고해주세요."
```

---

**작성일:** 2026-03-08  
**대상:** 회사 Cline 작업용  
**버전:** 1.0  
**상태:** ✅ 검토 완료

