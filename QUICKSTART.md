# 🚀 빠른 시작 가이드

## 사외 환경에서 5분 안에 시작하기

### 📋 준비물

```bash
# Python 3.10+ 확인
python --version

# Git 확인
git --version
```

---

## 🎯 시나리오별 사용법

### 시나리오 1️⃣: 템플릿으로 빠르게 테스트

**가장 추천하는 방법!**

```bash
# 1. 테스트 문서 생성
python create_test_doc.py "나의 첫 문서"

# 2. 미리보기 (실제 저장 안 함)
python export_agent_to_docs.py --input test_나의-첫-문서.txt --dry-run

# 3. 로컬에만 저장 (Git 제외)
python export_agent_to_docs.py --input test_나의-첫-문서.txt --skip-git

# 4. 결과 확인
cat docs/analysis/나의-첫-문서.md
```

**소요 시간: 1분**

---

### 시나리오 2️⃣: ChatGPT/Claude 활용

**AI로 실제 문서 생성하기**

#### Step 1: AI에게 요청

ChatGPT나 Claude에게 다음과 같이 요청:

```
다음 형식으로 "Python 베스트 프랙티스"에 대한 기술 문서를 작성해줘:

TITLE:
[문서 제목]

FILENAME:
[파일명-kebab-case]

CONTENT:
# [문서 제목]

[Markdown 형식의 본문...]
```

#### Step 2: 결과 저장

AI 응답을 복사하여 `my_doc.txt` 파일로 저장

#### Step 3: 실행

```bash
python export_agent_to_docs.py --input my_doc.txt --category guides
```

**소요 시간: 3분**

---

### 시나리오 3️⃣: 수동 작성

**직접 파일 만들어 테스트하기**

#### my_document.txt 생성

```txt
TITLE:
API 설계 원칙

FILENAME:
api-design-principles

CONTENT:
# API 설계 원칙

## REST API 설계

### 1. URL 설계
- 명사 사용
- 복수형 사용
- 소문자 사용

### 2. HTTP 메서드
- GET: 조회
- POST: 생성
- PUT: 전체 수정
- PATCH: 부분 수정
- DELETE: 삭제

## 예제

```python
# GET /api/users
# POST /api/users
# GET /api/users/{id}
# PUT /api/users/{id}
# DELETE /api/users/{id}
```

## 결론

일관된 API 설계가 중요합니다.
```

#### 실행

```bash
python export_agent_to_docs.py --input my_document.txt --category guides --skip-git
```

**소요 시간: 2분**

---

## 🎨 다양한 옵션 조합

### 케이스 A: Dry-run으로 안전하게 테스트

```bash
python export_agent_to_docs.py --input test.txt --dry-run
```

무엇이 실행될지 미리 확인만 하고 실제 변경은 하지 않습니다.

### 케이스 B: 로컬만 저장 (Git 제외)

```bash
python export_agent_to_docs.py --input test.txt --skip-git
```

파일만 저장하고 Git은 나중에 수동으로 관리하고 싶을 때

### 케이스 C: 전체 자동화 (저장 + Git + MkDocs)

```bash
python export_agent_to_docs.py --input test.txt --build
```

파일 저장 → Git push → MkDocs build까지 한 번에

### 케이스 D: 실시간 미리보기

```bash
python export_agent_to_docs.py --input test.txt --serve --skip-git
```

저장 후 `http://localhost:8000`에서 미리보기 (Ctrl+C로 종료)

### 케이스 E: 기존 파일 덮어쓰기

```bash
python export_agent_to_docs.py --input test.txt --overwrite
```

같은 파일명이 있으면 덮어쓰기 (기본은 timestamp 추가)

---

## 🔄 일반적인 워크플로우

### 개발 환경 (로컬 테스트)

```bash
# 1. 테스트 문서 생성
python create_test_doc.py "테스트 문서"

# 2. Dry-run 확인
python export_agent_to_docs.py --input test_테스트-문서.txt --dry-run

# 3. 로컬 저장만
python export_agent_to_docs.py --input test_테스트-문서.txt --skip-git

# 4. 미리보기
cd docs && python -m http.server 8000
```

### 프로덕션 환경 (실제 배포)

```bash
# 1. 문서 준비 (AI 또는 수동)
# my_doc.txt 생성

# 2. 최종 확인
python export_agent_to_docs.py --input my_doc.txt --dry-run

# 3. 배포
python export_agent_to_docs.py --input my_doc.txt --category guides
```

---

## 🎓 실전 예제

### 예제 1: 다수의 문서를 한 번에 처리

```bash
# 여러 테스트 문서 생성
python create_test_doc.py "문서 A" analysis
python create_test_doc.py "문서 B" guides
python create_test_doc.py "문서 C" reports

# 배치 처리 (Git은 마지막에 한 번만)
for file in test_*.txt; do
    python export_agent_to_docs.py --input "$file" --skip-git
done

# 한 번에 커밋
git add .
git commit -m "docs: batch import AI generated documents"
git push
```

### 예제 2: 카테고리별 정리

```bash
# analysis 카테고리
python export_agent_to_docs.py --input analysis_doc.txt --category analysis

# guides 카테고리
python export_agent_to_docs.py --input guide_doc.txt --category guides

# reports 카테고리
python export_agent_to_docs.py --input report_doc.txt --category reports
```

### 예제 3: MkDocs와 함께 사용

```bash
# 1. 문서 저장
python export_agent_to_docs.py --input doc.txt --skip-git

# 2. MkDocs로 미리보기
mkdocs serve

# 3. 확인 후 배포
git add .
git commit -m "docs: add new document"
git push

# 4. MkDocs 빌드 (GitHub Pages 등)
mkdocs gh-deploy
```

---

## ✅ 체크리스트

### 첫 실행 전

- [ ] Python 3.10+ 설치 확인
- [ ] Git 설치 확인
- [ ] GitHub 저장소 준비
- [ ] MkDocs 설치 (선택)

### 실행 중

- [ ] 입력 파일 형식 확인 (TITLE/FILENAME/CONTENT)
- [ ] 카테고리 선택
- [ ] 옵션 확인 (--dry-run, --skip-git 등)

### 실행 후

- [ ] 파일이 올바른 위치에 저장되었는지 확인
- [ ] Git 커밋이 정상적으로 되었는지 확인
- [ ] GitHub에 푸시되었는지 확인
- [ ] MkDocs에서 제대로 보이는지 확인

---

## 🆘 문제 해결

### Q: "입력 파일을 찾을 수 없습니다" 에러

```bash
# 현재 디렉토리 확인
ls -la

# 절대 경로 사용
python export_agent_to_docs.py --input /full/path/to/file.txt
```

### Q: Git push가 실패합니다

```bash
# 인증 확인
git config --list | grep user

# 저장소 확인
git remote -v

# 토큰 재설정 필요시
git remote set-url origin https://TOKEN@github.com/USER/REPO.git
```

### Q: 파일명이 이상하게 저장됩니다

FILENAME에 영문자와 숫자를 포함하세요. 특수문자는 자동으로 제거됩니다.

**예시:**
- ❌ `한글만` → 빈 문자열 에러
- ✅ `document-1` → 정상
- ✅ `my-doc-한글` → `my-doc-` 으로 저장

### Q: MkDocs 명령어가 없습니다

```bash
pip install mkdocs mkdocs-material
```

---

## 🎁 보너스 팁

### Tip 1: Alias 설정

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias export-doc='python /path/to/export_agent_to_docs.py'
alias create-doc='python /path/to/create_test_doc.py'

# 사용
export-doc --input test.txt --category guides
create-doc "새 문서" analysis
```

### Tip 2: VS Code Task 설정

`.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Export Agent to Docs",
      "type": "shell",
      "command": "python",
      "args": [
        "export_agent_to_docs.py",
        "--input",
        "${file}",
        "--category",
        "analysis"
      ]
    }
  ]
}
```

### Tip 3: 로그 파일 생성

```bash
python export_agent_to_docs.py --input test.txt 2>&1 | tee export.log
```

---

## 🎯 다음 단계

1. ✅ 기본 사용법 익히기
2. ✅ 다양한 옵션 테스트
3. ⬜ 클립보드 입력 추가
4. ⬜ Web UI 구축
5. ⬜ CI/CD 파이프라인 연동

---

## 📞 도움이 필요하신가요?

- 📖 [상세 가이드](TESTING_GUIDE.md)
- 📖 [README](README.md)
- 🐛 [Issues](https://github.com/miniforce1119/Documents/issues)

---

**Happy Documentation! 📝✨**
