# Agent Builder Documentation

Agent Builder 자동화 시스템에 오신 것을 환영합니다! 🎉

## 📚 소개

이 문서 사이트는 **Agent Builder to MkDocs 자동화 시스템**으로 생성된 문서들을 모아놓은 곳입니다.

### 🎯 주요 기능

- ✅ **자동 문서 생성**: Agent Builder 결과를 자동으로 파싱
- ✅ **카테고리별 정리**: 분석, 가이드, 리포트 등으로 분류
- ✅ **Git 연동**: 자동 커밋 및 푸시
- ✅ **실시간 미리보기**: MkDocs로 즉시 확인

## 📂 문서 카테고리

### 📊 분석 문서
프로젝트 분석, 데이터 분석 관련 문서

- [MkDocs Documentation Workflow](analysis/mkdocs-documentation-workflow.md)

### 📖 가이드
사용 가이드, 튜토리얼 문서

- [Agent Builder 자동화](guides/agent-builder.md)

## 🚀 시작하기

### 새 문서 생성 방법

```bash
# 1. 테스트 문서 생성
python create_test_doc.py "문서 제목" [카테고리]

# 2. 문서 저장 및 배포
python export_agent_to_docs.py --input test_문서-제목.txt --category guides
```

### 실시간 미리보기

```bash
# MkDocs 서버 시작
mkdocs serve

# http://localhost:8000 에서 확인
```

## 🔧 사용 가능한 카테고리

| 카테고리 | 설명 | 예시 |
|---------|------|------|
| `analysis` | 분석 문서 | 데이터 분석, 프로젝트 분석 |
| `guides` | 가이드 | 사용법, 튜토리얼 |
| `reports` | 리포트 | 보고서, 결과 문서 |
| `concepts` | 개념 | 용어 정리, 개념 설명 |

## 📝 문서 작성 형식

Agent Builder는 다음 형식으로 출력합니다:

```
TITLE:
문서 제목

FILENAME:
파일명-kebab-case

CONTENT:
# Markdown 형식의 내용
...
```

## 🎨 테마 및 기능

이 사이트는 **Material for MkDocs** 테마를 사용합니다.

### 주요 기능
- 🌓 다크 모드 지원
- 🔍 실시간 검색
- 📱 반응형 디자인
- 💻 코드 하이라이팅
- 📑 탭 네비게이션

## 🔗 관련 링크

- [GitHub Repository](https://github.com/miniforce1119/Documents)
- [MkDocs 공식 문서](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

## 📊 통계

현재 문서 수: **2개**

- 분석 문서: 1개
- 가이드: 1개

---

**마지막 업데이트**: 2026-03-07

**자동 생성**: Agent Builder Automation System
