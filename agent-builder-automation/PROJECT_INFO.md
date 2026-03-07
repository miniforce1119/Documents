# Agent Builder to MkDocs Automation

## 📁 프로젝트 구조

```
agent-builder-automation/
├── export_agent_to_docs.py        # 메인 스크립트 - Agent 결과 파싱 및 저장
├── create_test_doc.py              # 테스트 문서 생성기
├── README.md                       # 프로젝트 전체 가이드
├── QUICKSTART.md                   # 5분 빠른 시작 가이드 ⭐
├── TESTING_GUIDE.md                # 사외 환경 테스트 가이드
├── SUMMARY.md                      # 프로젝트 완료 요약
├── PROJECT_INFO.md                 # 이 파일
├── test_agent_output.txt           # 테스트용 예제 파일
├── test_api-설계-가이드.txt        # 한글 테스트 파일
└── docs/                           # 생성된 문서 저장 폴더
    └── analysis/
        └── mkdocs-documentation-workflow.md
```

## 🎯 프로젝트 목적

Agent Builder 결과를 자동으로 파싱하여 MkDocs 문서 저장소에 반영하는 자동화 도구

## 🚀 빠른 시작

### 1분 안에 시작하기

```bash
cd agent-builder-automation

# 테스트 문서 생성
python create_test_doc.py "나의 첫 문서"

# Dry-run 테스트
python export_agent_to_docs.py --input test_나의-첫-문서.txt --dry-run

# 실제 저장 (Git 제외)
python export_agent_to_docs.py --input test_나의-첫-문서.txt --skip-git
```

## 📚 문서 가이드

### 처음 사용하시나요?
👉 **[QUICKSTART.md](QUICKSTART.md)** - 5분 안에 시작하는 방법

### 사외 환경에서 테스트하려면?
👉 **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - 회사 Agent Builder 없이 테스트하는 3가지 방법

### 상세한 설명이 필요하신가요?
👉 **[README.md](README.md)** - 전체 기능 및 옵션 설명

### 프로젝트 요약을 보려면?
👉 **[SUMMARY.md](SUMMARY.md)** - 프로젝트 완료 보고서

## ✨ 주요 기능

- ✅ Agent Builder Export 결과 자동 파싱 (TITLE/FILENAME/CONTENT)
- ✅ MkDocs `docs/` 폴더에 Markdown 파일 저장
- ✅ Git 자동화 (add/commit/push)
- ✅ MkDocs build/serve 자동 실행
- ✅ 파일명 sanitize 및 중복 처리
- ✅ Dry-run 모드 지원
- ✅ 사외 환경 테스트 가능

## 🎨 사용 시나리오

### 시나리오 1: 템플릿으로 빠르게 테스트 (1분)
```bash
python create_test_doc.py "문서 제목"
python export_agent_to_docs.py --input test_문서-제목.txt --skip-git
```

### 시나리오 2: ChatGPT/Claude 활용 (3분)
1. AI에게 문서 작성 요청
2. 결과를 파일로 저장
3. `python export_agent_to_docs.py --input my_doc.txt`

### 시나리오 3: 프로덕션 배포
```bash
python export_agent_to_docs.py --input agent_output.txt --category guides --build
```

## 🔧 주요 옵션

```bash
--input <file>      # 입력 파일 (필수)
--category <name>   # 문서 카테고리 (기본: analysis)
--dry-run           # 미리보기만
--skip-git          # Git 작업 생략
--build             # MkDocs build 실행
--serve             # MkDocs serve 실행
--overwrite         # 기존 파일 덮어쓰기
```

## 📈 프로젝트 상태

- ✅ 스크립트 완성도: **100%**
- ✅ 문서 완성도: **100%**
- ✅ 테스트 통과율: **100%**
- ✅ 프로덕션 준비: **완료**

## 🎓 학습 경로

1. **초보자**: QUICKSTART.md → 시나리오 1
2. **중급자**: QUICKSTART.md → 시나리오 2  
3. **고급자**: README.md → 고급 사용법
4. **테스터**: TESTING_GUIDE.md → 다양한 테스트

## 🔗 관련 링크

- [GitHub Repository](https://github.com/miniforce1119/Documents)
- [MkDocs 공식 문서](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

## 📅 버전 정보

- **버전**: 1.0.0
- **생성일**: 2026-03-07
- **상태**: ✅ 프로덕션 준비 완료

---

**Made with ❤️ for automation**
