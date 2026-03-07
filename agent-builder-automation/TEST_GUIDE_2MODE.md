# 2-Mode 시스템 테스트 가이드

## 📋 개요

현재 시스템은 **2가지 입력 모드**를 지원합니다:

- **Mode A**: Agent Builder Direct Import (정형 포맷)
- **Mode B**: External AI Reformat (자유 형식)

두 모드 모두 최종적으로 **동일한 표준 포맷**으로 정규화되어 동일한 Inbox/Publish 흐름을 따릅니다.

---

## 🚀 시스템 시작

### **1. Streamlit 앱 실행**

```bash
cd /path/to/agent-builder-automation
streamlit run doc_review_app.py
```

### **2. MkDocs 서버 실행** (선택사항)

```bash
mkdocs serve --dev-addr=0.0.0.0:8000
```

### **3. 접속**

- **Streamlit 앱:** http://localhost:8501
- **MkDocs 서버:** http://localhost:8000

---

## 🧪 Test Case 1: Mode A (Agent Builder)

### **목적**
사내 Agent Builder의 정형화된 결과를 직접 처리

### **입력 데이터**

```
TITLE:
Kubernetes 배포 전략

FILENAME:
kubernetes-deployment-strategy

CONTENT:
# Kubernetes 배포 전략

> 생성일: 2026-03-07
> 카테고리: concepts

## 개요

Kubernetes에서 애플리케이션을 배포하는 다양한 전략을 설명합니다.

## 주요 배포 전략

### 1. Rolling Update

점진적으로 Pod를 교체하는 방식

### 2. Blue-Green Deployment

두 개의 환경을 번갈아 전환

### 3. Canary Deployment

일부 사용자에게만 먼저 배포

## 결론

상황에 맞는 배포 전략을 선택하는 것이 중요합니다.
```

### **테스트 절차**

1. **Streamlit 앱 접속**
2. **"📥 Save to Inbox" 탭** 클릭
3. **입력 모드: "Agent Builder (정형)" 선택**
4. 위의 입력 데이터를 텍스트 영역에 붙여넣기
5. **"🔍 Parse & Preview" 클릭**
6. **결과 확인:**
   - ✅ 제목: "Kubernetes 배포 전략"
   - ✅ 파일명: "kubernetes-deployment-strategy"
   - ✅ Markdown Preview가 정상 표시됨
7. **카테고리: "concepts" 선택**
8. **태그 입력:** `kubernetes, deployment, devops`
9. **"💾 Save to Inbox" 클릭**
10. **성공 메시지 확인**

### **검증**

```bash
# Inbox에 파일이 생성되었는지 확인
ls -la inbox/

# 파일 내용 확인
cat inbox/20260307-*.md
```

---

## 🧪 Test Case 2: Mode B (External AI - 간단한 텍스트)

### **목적**
외부 AI의 자유 형식 텍스트를 표준 포맷으로 재구성

### **입력 데이터**

```
Docker 컨테이너 최적화 방법

1. 멀티 스테이지 빌드
이미지 크기를 줄이고 빌드 속도를 높일 수 있습니다.

2. 레이어 캐싱 활용
자주 변경되지 않는 명령어를 먼저 실행하세요.

3. .dockerignore 사용
불필요한 파일을 제외하여 이미지 크기를 줄입니다.

4. Alpine 이미지 사용
경량 베이스 이미지를 사용하면 전체 크기가 줄어듭니다.
```

### **테스트 절차**

1. **"📥 Save to Inbox" 탭**
2. **입력 모드: "외부 AI (재구성)" 선택**
3. 위의 입력 데이터 붙여넣기
4. **"🔄 Reformat & Preview" 클릭**
5. **결과 확인:**
   - ✅ 제목이 자동 생성됨 (예: "Docker 컨테이너 최적화 방법")
   - ✅ 파일명이 자동 생성됨 (예: "docker-컨테이너-최적화-방법")
   - ✅ Markdown으로 구조화됨
   - ✅ 헤더, 리스트 등이 적절히 변환됨
6. **카테고리: "guides" 선택**
7. **"💾 Save to Inbox" 클릭**

### **예상 출력 (Mock 변환)**

```markdown
# Docker 컨테이너 최적화 방법

> 생성일: 2026-03-07
> 출처: 외부 AI

## 1. 멀티 스테이지 빌드

이미지 크기를 줄이고 빌드 속도를 높일 수 있습니다.

## 2. 레이어 캐싱 활용

자주 변경되지 않는 명령어를 먼저 실행하세요.

...
```

---

## 🧪 Test Case 3: Mode B (External AI - 복잡한 텍스트)

### **목적**
코드 블록, 표 등이 포함된 복잡한 텍스트 처리

### **입력 데이터**

```
Python에서 비동기 프로그래밍 하는 방법

asyncio를 사용하면 비동기 작업을 쉽게 처리할 수 있습니다.

기본 사용법:
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(main())

성능 비교:
동기 방식: 10초
비동기 방식: 2초

주의사항:
- await은 async 함수 안에서만 사용 가능
- asyncio.run()은 Python 3.7 이상에서만 사용
```

### **테스트 절차**

1. **Mode B 선택**
2. 위의 텍스트 붙여넣기
3. **"🔄 Reformat & Preview"**
4. **검증:**
   - ✅ 코드 블록이 유지되는가?
   - ✅ 구조가 논리적으로 재구성되는가?
   - ✅ 주의사항이 리스트로 변환되는가?

---

## 🧪 Test Case 4: Review Inbox

### **목적**
Inbox에 저장된 문서를 검토하고 Publish

### **테스트 절차**

1. **"📋 Review Inbox" 탭** 클릭
2. **저장된 문서 선택**
3. **메타데이터 확인:**
   - 제목
   - 파일명
   - 카테고리
   - 생성일
4. **Preview 확인** (Markdown 렌더링)
5. **필요시 카테고리 변경**
6. **"🚀 Publish" 클릭**
7. **성공 메시지 확인:**
   - ✅ "Git push 및 GitHub Pages 배포 완료!"
8. **약 30초~1분 대기** (배포 시간)

### **검증**

```bash
# docs 폴더 확인
ls -la docs/concepts/
ls -la docs/guides/

# Git 커밋 확인
git log --oneline -5
```

---

## 🧪 Test Case 5: MkDocs 확인

### **목적**
발행된 문서가 MkDocs 사이트에 정상 표시되는지 확인

### **로컬 MkDocs**

1. MkDocs 서버 실행 중인지 확인
2. http://localhost:8000 접속
3. **네비게이션 메뉴 확인:**
   - Analysis
   - Concepts
   - Guides
   - Reports
4. **발행한 문서 클릭**
5. **렌더링 확인:**
   - ✅ 헤더가 정상 표시되는가?
   - ✅ 코드 블록이 하이라이팅되는가?
   - ✅ 표가 정상 렌더링되는가?
   - ✅ 리스트가 제대로 표시되는가?

### **GitHub Pages** (배포 후 2~3분)

1. https://your-username.github.io/Documents/ 접속
2. 동일한 검증 수행
3. **브라우저 캐시 강제 새로고침:**
   - Windows: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

---

## 🧪 Test Case 6: 에러 케이스

### **6-1. 잘못된 포맷 (Mode A)**

**입력:**
```
이것은 잘못된 포맷입니다.
TITLE이나 FILENAME이 없습니다.
```

**예상 결과:**
- ❌ "TITLE/FILENAME/CONTENT 블록을 찾을 수 없습니다."

### **6-2. 빈 텍스트**

**입력:** (빈 칸)

**예상 결과:**
- ⚠️ "텍스트를 입력해주세요."

### **6-3. 너무 짧은 텍스트 (Mode B)**

**입력:**
```
안녕
```

**예상 결과:**
- ⚠️ 처리는 되지만 품질이 낮을 수 있음
- 제목: "안녕"
- 내용이 거의 없음

---

## 🧪 Test Case 7: 전체 워크플로우

### **목적**
전체 시스템 흐름을 처음부터 끝까지 테스트

### **시나리오**

```
외부 AI에서 답변을 받음
  ↓
Mode B로 Streamlit에 붙여넣기
  ↓
Reformat & Preview
  ↓
카테고리 선택 (guides)
  ↓
Save to Inbox
  ↓
Review Inbox에서 확인
  ↓
Publish 클릭
  ↓
30초~1분 대기
  ↓
로컬 MkDocs 확인 (즉시)
  ↓
GitHub Pages 확인 (2~3분 후)
```

### **예상 소요 시간**

- 입력 & Reformat: ~10초
- Save to Inbox: ~1초
- Review: ~30초
- Publish: ~30초~1분
- **총 소요 시간: 약 2~3분**

---

## ✅ 체크리스트

### **기본 기능**
- [ ] Mode A (Agent Builder) 정상 작동
- [ ] Mode B (External AI) 정상 작동
- [ ] Parse/Reformat 성공
- [ ] Preview 정상 표시
- [ ] Save to Inbox 성공
- [ ] Review Inbox 정상 작동
- [ ] Publish 성공
- [ ] Git push 자동 실행
- [ ] MkDocs gh-deploy 자동 실행

### **문서 렌더링**
- [ ] 헤더 정상 표시
- [ ] 코드 블록 하이라이팅
- [ ] 표 정상 렌더링
- [ ] 리스트 정상 표시
- [ ] 링크 작동

### **카테고리별 확인**
- [ ] analysis 폴더에 문서 생성
- [ ] concepts 폴더에 문서 생성
- [ ] guides 폴더에 문서 생성
- [ ] reports 폴더에 문서 생성

### **MkDocs 사이트**
- [ ] 로컬 MkDocs 정상 표시
- [ ] GitHub Pages 정상 배포
- [ ] 네비게이션 메뉴 정상
- [ ] 검색 기능 작동 (있는 경우)

---

## 🐛 문제 해결

### **"파싱 실패" 에러**

**원인:** Mode A에서 TITLE/FILENAME/CONTENT 포맷이 아님

**해결:**
1. 입력 포맷 확인
2. Mode B로 전환 시도

### **"처리 실패" 에러 (Mode B)**

**원인:** 
- Mock 변환 로직 오류
- 텍스트가 너무 짧거나 이상함

**해결:**
1. 입력 텍스트 확인
2. 더 많은 내용 제공
3. Mode A로 전환 고려

### **"Git push 실패"**

**원인:** Git 권한 문제

**해결:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### **"GitHub Pages 업데이트 안 됨"**

**원인:**
- 아직 배포 중 (2~3분 소요)
- 브라우저 캐시

**해결:**
1. 2~3분 대기
2. 브라우저 캐시 강제 새로고침
3. GitHub Actions 확인: https://github.com/user/repo/actions

---

## 📊 성능 벤치마크

### **처리 시간**

| 단계 | 소요 시간 |
|------|----------|
| Parse (Mode A) | < 1초 |
| Reformat (Mode B - Mock) | < 1초 |
| Reformat (Mode B - Real API) | 3~10초 (예상) |
| Save to Inbox | < 1초 |
| Publish | 30초~1분 |
| GitHub Pages 배포 | 2~3분 |

### **문서 크기 제한**

- **최소:** 10자 (권장하지 않음)
- **권장:** 100자 이상
- **최대:** 제한 없음 (단, API 타임아웃 고려)

---

## 🎯 성공 기준

모든 테스트 케이스가 통과하면 **2-Mode 시스템이 정상 작동**하는 것입니다!

다음 단계:
1. 사내 환경에서 Reformat Agent API 연동
2. 실제 사용자 테스트
3. 피드백 수집 및 개선

---

**작성일:** 2026-03-07  
**버전:** 1.0
