# AI Document Review & Publish System

AI 생성 문서를 검토하고 발행하는 **2-Mode 문서화 시스템**입니다.

## 🎯 핵심 철학

> "AI 생성 지식을 문서 자산으로 변환하는 검토/발행 시스템"

단순 저장 도구가 아닌, 유용한 AI 결과를 선별하고 정규화하여 축적하는 시스템입니다.

## ⚡ 2-Mode 시스템

### **Mode A: Agent Builder Direct Import**
- 사내 Agent Builder의 정형화된 결과 직접 처리
- `TITLE` / `FILENAME` / `CONTENT` 포맷

### **Mode B: External AI Reformat**
- ChatGPT/Claude 등 외부 AI 결과 재구성
- 자유 형식 텍스트 → 표준 Markdown 문서

**두 모드 모두 동일한 표준 포맷으로 정규화됩니다.**

## 🚀 주요 기능

- ✅ **2가지 입력 모드** (정형/비정형)
- ✅ **Inbox/Review/Publish 워크플로우**
- ✅ **Streamlit 기반 UI** (검토 중심 UX)
- ✅ **자동 Git 통합** (commit/push)
- ✅ **GitHub Pages 자동 배포** (MkDocs)
- ✅ **실시간 Preview** (Markdown 렌더링)

## 📦 필수 요구사항

- Python 3.10+
- Git
- MkDocs (선택사항)

```bash
pip install mkdocs mkdocs-material
```

## 🚀 빠른 시작

### 1. 필수 패키지 설치

```bash
pip install streamlit mkdocs mkdocs-material
```

### 2. Streamlit 앱 실행

```bash
cd agent-builder-automation
streamlit run doc_review_app.py
```

### 3. 브라우저에서 접속

- **Streamlit 앱:** http://localhost:8501
- **MkDocs 서버:** http://localhost:8000 (선택사항)

### 4. 문서 생성 워크플로우

```
1. "📥 Save to Inbox" 탭 클릭
2. 입력 모드 선택:
   - "Agent Builder (정형)"
   - "외부 AI (재구성)"
3. 텍스트 붙여넣기
4. Parse/Reformat & Preview
5. Save to Inbox
6. "📋 Review Inbox"에서 검토
7. "🚀 Publish" 클릭
8. 자동으로 GitHub Pages 배포!
```

## 📖 사용 방법

### 기본 사용법

```bash
python export_agent_to_docs.py --input <파일경로> [옵션]
```

### 주요 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--input` | Agent 출력 파일 경로 (필수) | - |
| `--repo` | Git 저장소 루트 경로 | `.` |
| `--category` | docs 하위 카테고리 | `analysis` |
| `--overwrite` | 동일 파일 덮어쓰기 | `False` |
| `--dry-run` | 실제 저장 없이 시뮬레이션 | `False` |
| `--skip-git` | Git 작업 생략 | `False` |
| `--build` | MkDocs build 실행 | `False` |
| `--serve` | MkDocs serve 실행 | `False` |

### 사용 예시

```bash
# 기본 사용
python export_agent_to_docs.py --input agent_output.txt

# 카테고리 지정
python export_agent_to_docs.py --input agent_output.txt --category guides

# Git 제외하고 로컬만 저장
python export_agent_to_docs.py --input agent_output.txt --skip-git

# 저장 후 MkDocs build
python export_agent_to_docs.py --input agent_output.txt --build

# 저장 후 MkDocs serve (미리보기)
python export_agent_to_docs.py --input agent_output.txt --serve

# Dry-run 테스트
python export_agent_to_docs.py --input agent_output.txt --dry-run

# 기존 파일 덮어쓰기
python export_agent_to_docs.py --input agent_output.txt --overwrite
```

## 📝 입력 파일 형식

Agent Builder의 출력 형식:

```txt
TITLE:
문서 제목

FILENAME:
파일명-kebab-case

CONTENT:
# Markdown 문서

본문 내용...
```

## 🔧 사외 환경 테스트 방법

회사 Agent Builder 없이 테스트하는 방법은 `TESTING_GUIDE.md`를 참고하세요.

### 방법 1: 템플릿 생성기 사용 (추천)

```bash
python create_test_doc.py "문서 제목" [카테고리]
```

### 방법 2: 수동 파일 생성

`test_input.txt` 파일을 만들고 위 형식으로 작성합니다.

### 방법 3: ChatGPT/Claude 활용

AI에게 위 형식으로 문서를 요청하고 결과를 파일로 저장합니다.

## 📁 프로젝트 구조

```
repo-root/
├── mkdocs.yml                    # MkDocs 설정
├── docs/                         # 문서 폴더
│   ├── index.md                 # 홈페이지
│   ├── analysis/                # 분석 문서
│   ├── guides/                  # 가이드 문서
│   ├── reports/                 # 리포트 문서
│   └── concepts/                # 개념 문서
├── export_agent_to_docs.py      # 메인 스크립트
├── create_test_doc.py           # 테스트 생성기
├── README.md                    # 이 파일
└── TESTING_GUIDE.md             # 상세 테스트 가이드
```

## 🎬 Workflow

```
Agent Builder
    ↓
Export 결과 생성
    ↓
Python Script (export_agent_to_docs.py)
    ↓
① 파일 파싱 (TITLE/FILENAME/CONTENT)
    ↓
② Markdown 저장 (docs/category/filename.md)
    ↓
③ Git 자동화 (add/commit/push)
    ↓
④ MkDocs 처리 (build/serve)
    ↓
✅ 완료
```

## 🔍 파일명 Sanitize 규칙

- 소문자로 변환
- 공백을 하이픈(`-`)으로 변환
- 영문자, 숫자, 하이픈만 유지
- 연속된 하이픈을 하나로 통합
- 앞뒤 하이픈 제거

**예시:**
- `"My First Document"` → `my-first-document`
- `"API 설계 가이드 (v2.0)"` → `api-v20`
- `"Python Best Practices!!!"` → `python-best-practices`

## 🛡️ 에러 처리

### 파일명이 비정상인 경우

스크립트가 자동으로 sanitize 처리하지만, 결과가 빈 문자열이면 에러가 발생합니다.

**해결책:** FILENAME에 영문자나 숫자를 포함하세요.

### Git push 실패

GitHub 인증이 필요합니다.

```bash
# GitHub 토큰 설정 확인
git config --list | grep user

# 필요시 재설정
git remote set-url origin https://TOKEN@github.com/USER/REPO.git
```

### MkDocs 미설치

```bash
pip install mkdocs mkdocs-material
```

## 🎓 고급 사용법

### 배치 처리

여러 문서를 한 번에 처리:

```bash
for file in test_*.txt; do
    python export_agent_to_docs.py --input "$file" --category analysis --skip-git
done

# 마지막에 한 번만 git commit
git add .
git commit -m "batch import AI docs"
git push
```

### 커스텀 Commit 메시지

스크립트를 수정하여 commit 메시지를 커스터마이즈할 수 있습니다:

```python
# export_agent_to_docs.py의 git_commit_and_push 함수 수정
commit_message = f"docs: add {filename} [AI-generated]"
```

### CI/CD 연동

GitHub Actions에서 실행:

```yaml
# .github/workflows/import-docs.yml
name: Import AI Docs

on:
  workflow_dispatch:
    inputs:
      doc_url:
        description: 'Agent output file URL'
        required: true

jobs:
  import:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Download and process
        run: |
          curl -o agent_output.txt ${{ github.event.inputs.doc_url }}
          python export_agent_to_docs.py --input agent_output.txt
```

## 🐛 디버깅

### Verbose 모드

스크립트의 print 문을 통해 진행 상황을 확인할 수 있습니다:

```bash
python export_agent_to_docs.py --input test.txt --dry-run
```

### 로그 파일 생성

```bash
python export_agent_to_docs.py --input test.txt 2>&1 | tee import.log
```

## 🤝 기여

이슈나 개선 제안은 GitHub Issues를 통해 제출해주세요.

## 📄 라이선스

MIT License

## 🔗 참고 자료

- [MkDocs 공식 문서](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Python argparse](https://docs.python.org/3/library/argparse.html)

## 📞 문의

문제가 발생하거나 질문이 있으시면 Issues 탭에 등록해주세요.

---

**Made with ❤️ for automation**
