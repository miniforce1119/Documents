# 📝 Document Review & Publish App 가이드

## 🎯 개요

Streamlit 기반 **Inbox/Publish 구조**의 문서 검토 및 발행 시스템입니다.

### 핵심 철학

```
생성 → 검토 → 발행
  ↓      ↓      ↓
Agent → Inbox → Docs
```

**문서를 바로 저장하지 않고, Inbox에서 검토 후 발행합니다.**

---

## 🚀 빠른 시작

### 1️⃣ 앱 실행

```bash
cd agent-builder-automation
streamlit run doc_review_app.py
```

**접속 URL**: http://localhost:8501

---

## 📋 사용 방법

### Workflow 1: Save to Inbox (문서 저장)

#### Step 1: Agent Builder 결과 복사

Agent Builder에서 질문 후 결과를 다음 형식으로 받습니다:

```
TITLE:
API 설계 가이드

FILENAME:
api-design-guide

CONTENT:
# API 설계 가이드

## REST API 설계 원칙
...
```

#### Step 2: 앱에 붙여넣기

1. **"Save to Inbox" 탭** 클릭
2. 텍스트 영역에 **붙여넣기**
3. **"Parse & Preview"** 버튼 클릭

#### Step 3: Preview 확인

- **좌측**: 메타데이터 (제목, 파일명, 카테고리, 태그)
- **우측**: Markdown 미리보기

#### Step 4: 카테고리 선택

- `analysis` - 분석 문서
- `guides` - 가이드
- `reports` - 리포트
- `concepts` - 개념 설명

#### Step 5: Save to Inbox

**"Save to Inbox"** 버튼 클릭

✅ Inbox에 저장 완료!

---

### Workflow 2: Review Inbox (검토 및 발행)

#### Step 1: Inbox 문서 확인

1. **"Review Inbox" 탭** 클릭
2. 문서 목록 확인
3. 검토할 문서 선택

#### Step 2: 문서 검토

- **좌측**: 메타데이터
- **우측**: Markdown Preview

**검토 질문**:
- ✅ 저장할 가치가 있나?
- ✅ 내용이 정확한가?
- ✅ 중복 문서는 없나?
- ✅ 카테고리가 맞나?

#### Step 3: 발행 결정

**옵션 1: Publish** 🚀
- 제목/파일명 수정 가능
- 카테고리 변경 가능
- "Publish" 버튼 클릭
- → `docs/` 폴더로 이동
- → Git push (옵션)

**옵션 2: Delete** 🗑️
- 가치가 없으면 삭제
- "Delete" 버튼 클릭

---

### Workflow 3: Published Docs (발행 문서 확인)

1. **"Published Docs" 탭** 클릭
2. 발행된 문서 목록 확인
3. 문서 내용 미리보기

---

## 📂 폴더 구조

```
agent-builder-automation/
├── doc_review_app.py          # Streamlit 앱
├── inbox/                      # 📥 검토 대기 문서
│   └── 20260307-120000_api-design-guide.md
├── published/                  # 📤 발행된 문서 백업
│   └── api-design-guide.md
└── docs/                       # 📚 MkDocs 문서 (Git 관리)
    ├── analysis/
    ├── guides/
    │   └── api-design-guide.md
    ├── reports/
    └── concepts/
```

### 폴더 역할

| 폴더 | 역할 | Git 관리 |
|------|------|----------|
| `inbox/` | 검토 대기 | ❌ (로컬만) |
| `published/` | 발행 백업 | ❌ (로컬만) |
| `docs/` | 실제 문서 | ✅ (Git push) |

---

## 🎨 UI 구성

### Tab 1: Save to Inbox

```
┌─────────────────────────────────────────────┐
│  📥 Agent 결과를 Inbox에 저장               │
├─────────────────────────────────────────────┤
│  [Agent Builder 결과 붙여넣기]              │
│  ┌───────────────────────────────────────┐  │
│  │ TITLE:                                │  │
│  │ ...                                   │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  [🔍 Parse & Preview]                       │
│                                              │
│  Preview:                                    │
│  ┌──────────────┬──────────────────────┐   │
│  │ 메타데이터   │  Markdown Preview    │   │
│  │ • 제목       │  # 문서 제목         │   │
│  │ • 파일명     │  ...                 │   │
│  │ • 카테고리   │                      │   │
│  └──────────────┴──────────────────────┘   │
│                                              │
│  [💾 Save to Inbox] [🗑️ Clear]             │
└─────────────────────────────────────────────┘
```

### Tab 2: Review Inbox

```
┌─────────────────────────────────────────────┐
│  📋 Inbox 문서 검토                         │
├─────────────────────────────────────────────┤
│  총 3개의 문서                              │
│  [문서 선택 드롭다운]                       │
│                                              │
│  ┌──────────────┬──────────────────────┐   │
│  │ 메타데이터   │  Preview             │   │
│  │ • 제목       │  # 문서 내용         │   │
│  │ • 파일명     │  ...                 │   │
│  │ • 카테고리   │                      │   │
│  │              │                      │   │
│  │ 발행 설정:   │                      │   │
│  │ [제목 수정]  │                      │   │
│  │ [파일명]     │                      │   │
│  │ [카테고리]   │                      │   │
│  └──────────────┴──────────────────────┘   │
│                                              │
│  [🚀 Publish] [🗑️ Delete]                  │
└─────────────────────────────────────────────┘
```

### Tab 3: Published Docs

```
┌─────────────────────────────────────────────┐
│  📊 발행된 문서                             │
├─────────────────────────────────────────────┤
│  총 5개의 발행 문서                         │
│                                              │
│  ▼ api-design-guide.md                      │
│    # API 설계 가이드                        │
│    ...                                       │
│    [🔗 Open in docs]                        │
│                                              │
│  ▼ data-analysis-report.md                  │
│    # 데이터 분석 리포트                     │
│    ...                                       │
└─────────────────────────────────────────────┘
```

### Sidebar

```
┌─────────────────────┐
│  ⚙️ 설정            │
├─────────────────────┤
│  📂 경로            │
│  Inbox: inbox/      │
│  Published: ...     │
│  Docs: docs/        │
│                     │
│  📊 통계            │
│  Inbox: 3           │
│  Published: 5       │
│                     │
│  🔗 링크            │
│  📖 GitHub          │
│  🌐 Docs Site       │
│                     │
│  [🔄 Refresh]       │
└─────────────────────┘
```

---

## 💡 사용 시나리오

### 시나리오 1: 일반적인 문서 발행

```
1. Agent Builder에서 "API 설계 가이드" 질문
2. 결과 복사
3. Streamlit 앱 → Save to Inbox
4. 카테고리 "guides" 선택
5. Save
6. Review Inbox 탭으로 이동
7. 문서 확인
8. Publish 클릭
9. ✅ docs/guides/api-design-guide.md 생성
10. Git push 자동 실행
```

### 시나리오 2: 여러 문서 검토 후 선별 발행

```
1. 5개의 문서를 Inbox에 저장
2. Review Inbox에서 하나씩 검토
3. 가치 있는 3개만 Publish
4. 나머지 2개는 Delete
5. ✅ 품질 관리 완료
```

### 시나리오 3: 메타데이터 수정 후 발행

```
1. Inbox에서 문서 선택
2. 제목 수정: "API 설계" → "RESTful API 설계 원칙"
3. 파일명 수정: "api" → "restful-api-design"
4. 카테고리 변경: analysis → guides
5. Publish
6. ✅ 정확한 메타데이터로 발행
```

---

## 🔧 고급 기능

### 1. YAML Frontmatter

Inbox에 저장된 파일은 자동으로 메타데이터가 추가됩니다:

```yaml
---
title: API 설계 가이드
filename: api-design-guide
category: guides
tags: api, rest, design
created: 20260307-120000
status: inbox
---

# API 설계 가이드
...
```

### 2. Git 자동화

Publish 시 자동으로:
1. `git add .`
2. `git commit -m "docs: publish {filename}"`
3. `git push`

### 3. 파일명 Sanitize

자동으로 파일명을 정리합니다:
- 공백 → 하이픈
- 특수문자 제거
- 소문자 변환
- 한글 유지

**예시**:
- `"API 설계 가이드 (v2.0)"` → `"api-설계-가이드-v20"`

---

## 📊 장점

### ✅ 문서 품질 관리
- 바로 저장하지 않고 검토 후 발행
- 저가치 문서 필터링

### ✅ 유연한 메타데이터
- 제목/파일명 수정 가능
- 카테고리 변경 가능
- 태그 추가 가능

### ✅ 안전한 Workflow
- Inbox → Published → Docs 3단계
- 삭제 전 확인 가능
- 실수 방지

### ✅ 직관적인 UX
- 웹 기반 UI
- 실시간 Preview
- 버튼 클릭만으로 완료

### ✅ Git 자동화
- 수동 commit 불필요
- 자동 push
- 히스토리 관리

---

## 🐛 문제 해결

### 문제 1: 앱이 실행되지 않음

**해결**:
```bash
pip install streamlit
streamlit run doc_review_app.py
```

### 문제 2: Git push 실패

**해결**:
```bash
# GitHub 인증 확인
git config --list | grep user

# 필요시 재설정
# (이미 설정되어 있음)
```

### 문제 3: 파싱 실패

**원인**: Agent 결과 형식이 맞지 않음

**해결**: `TITLE:`, `FILENAME:`, `CONTENT:` 형식 확인

---

## 🎯 다음 단계 (확장 가능)

### Phase 1: 현재 (✅ 완료)
- Inbox/Publish 구조
- Streamlit UI
- Git 자동화

### Phase 2: 향후 개선
- 🔍 **검색 기능**: Inbox 문서 검색
- 🏷️ **태그 관리**: 태그별 필터링
- 📝 **Markdown 편집**: 앱 내에서 수정
- 🔄 **중복 감지**: 유사 문서 확인
- 📊 **통계 대시보드**: 문서 생성 추이

### Phase 3: 고급 기능
- 🤖 **AI 카테고리 자동 분류**
- 🔗 **Agent Builder 직접 연동**
- 👥 **다중 사용자 지원**
- 📱 **모바일 최적화**

---

## 🎉 완료!

**Document Review & Publish App이 준비되었습니다!**

**접속 URL**: http://localhost:8501

**주요 특징**:
- ✅ Inbox/Publish 구조
- ✅ 웹 기반 UI
- ✅ 실시간 Preview
- ✅ Git 자동화
- ✅ 문서 품질 관리

**지금 바로 사용해보세요!** 🚀
