# GitHub Pages 배포 가이드

## 🎯 개요

이 문서는 MkDocs 사이트를 GitHub Pages로 자동 배포하는 방법을 설명합니다.

## 🚀 자동 배포 설정 (GitHub Actions)

### ✅ 이미 완료된 작업

다음 파일들이 이미 설정되어 있습니다:

1. **`.github/workflows/deploy-docs.yml`** - GitHub Actions 워크플로우
2. **`mkdocs.yml`** - GitHub Pages 설정 포함

### 📋 GitHub 저장소 설정

#### 1단계: GitHub Pages 활성화

1. GitHub 저장소 페이지로 이동
   - https://github.com/miniforce1119/Documents

2. **Settings** 클릭

3. 왼쪽 메뉴에서 **Pages** 클릭

4. **Source** 섹션에서:
   - **Deploy from a branch** 선택
   - **Branch**: `gh-pages` 선택
   - **Folder**: `/ (root)` 선택
   - **Save** 클릭

#### 2단계: GitHub Actions 권한 확인

1. **Settings** → **Actions** → **General**

2. **Workflow permissions** 섹션에서:
   - ✅ **Read and write permissions** 선택
   - ✅ **Allow GitHub Actions to create and approve pull requests** 체크
   - **Save** 클릭

### 🔄 배포 트리거

다음 경우에 자동으로 배포됩니다:

#### 자동 배포 (권장)
```bash
# docs 폴더나 mkdocs.yml 변경 후 push
cd agent-builder-automation
python export_agent_to_docs.py --input test.txt --category guides
# 자동으로 git push되면 GitHub Actions 실행!
```

#### 수동 배포
1. GitHub 저장소 페이지
2. **Actions** 탭 클릭
3. **Deploy MkDocs to GitHub Pages** 워크플로우 선택
4. **Run workflow** 버튼 클릭

## 📱 배포 후 확인

### 1. GitHub Actions 상태 확인

1. 저장소 **Actions** 탭
2. 최근 워크플로우 실행 확인
3. ✅ 녹색 체크: 배포 성공
4. ❌ 빨간 X: 배포 실패 (로그 확인)

### 2. 사이트 접속

배포 완료 후 다음 URL에서 확인:

**🌐 https://miniforce1119.github.io/Documents/**

> **참고**: 첫 배포는 5-10분 정도 소요될 수 있습니다.

## 🔧 워크플로우 상세 설명

### `.github/workflows/deploy-docs.yml`

```yaml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - 'agent-builder-automation/docs/**'
      - 'agent-builder-automation/mkdocs.yml'
      - '.github/workflows/deploy-docs.yml'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - Checkout repository
      - Setup Python 3.12
      - Install MkDocs
      - Deploy to gh-pages branch
```

### 주요 기능

- ✅ **자동 트리거**: docs 폴더 변경 시 자동 실행
- ✅ **수동 실행**: workflow_dispatch로 수동 실행 가능
- ✅ **캐싱**: pip 캐시로 빌드 속도 향상
- ✅ **자동 배포**: gh-pages 브랜치에 자동 푸시

## 📊 전체 워크플로우

```
코드 작성/수정
     ↓
Python 스크립트 실행
export_agent_to_docs.py
     ↓
docs/ 폴더에 .md 파일 저장
     ↓
Git commit & push
     ↓
GitHub Actions 자동 트리거
     ↓
MkDocs build
     ↓
gh-pages 브랜치에 배포
     ↓
GitHub Pages 자동 업데이트
     ↓
🌐 사이트 갱신 완료!
```

## 🎯 실전 사용 예시

### 시나리오 1: 새 문서 추가

```bash
# 1. 테스트 문서 생성
cd agent-builder-automation
python create_test_doc.py "API 설계 가이드" guides

# 2. 저장 및 배포 (자동)
python export_agent_to_docs.py --input test_api-설계-가이드.txt --category guides

# 3. GitHub Actions 자동 실행
# (약 2-3분 후)

# 4. 사이트 확인
# https://miniforce1119.github.io/Documents/
```

### 시나리오 2: 여러 문서 배치 추가

```bash
# 1. 여러 문서 생성
python create_test_doc.py "문서 A" analysis
python create_test_doc.py "문서 B" guides
python create_test_doc.py "문서 C" reports

# 2. 배치 저장 (git 제외)
for file in test_*.txt; do
    python export_agent_to_docs.py --input "$file" --skip-git
done

# 3. 한 번에 커밋 & 푸시
git add .
git commit -m "docs: add multiple AI generated documents"
git push

# 4. GitHub Actions 자동 실행
```

## 🐛 문제 해결

### 문제 1: Actions 워크플로우가 실행되지 않음

**원인**: GitHub Actions 권한 부족

**해결**:
1. Settings → Actions → General
2. Workflow permissions → Read and write 선택

### 문제 2: gh-pages 브랜치 생성 실패

**원인**: 권한 문제

**해결**:
```bash
# 로컬에서 수동으로 첫 배포
cd agent-builder-automation
mkdocs gh-deploy --force

# 이후에는 GitHub Actions가 자동으로 처리
```

### 문제 3: 사이트가 404 에러

**원인**: GitHub Pages 브랜치 설정 오류

**해결**:
1. Settings → Pages
2. Source를 `gh-pages` 브랜치로 변경
3. 5-10분 대기

### 문제 4: 빌드는 성공하지만 사이트가 갱신 안 됨

**원인**: GitHub Pages 캐시

**해결**:
1. 브라우저 캐시 삭제 (Ctrl+Shift+R)
2. 5분 정도 대기
3. Incognito 모드로 확인

## 📈 배포 상태 뱃지

README에 배포 상태 뱃지를 추가할 수 있습니다:

```markdown
[![Deploy MkDocs](https://github.com/miniforce1119/Documents/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/miniforce1119/Documents/actions/workflows/deploy-docs.yml)
```

결과:
[![Deploy MkDocs](https://github.com/miniforce1119/Documents/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/miniforce1119/Documents/actions/workflows/deploy-docs.yml)

## 🎨 커스텀 도메인 (선택사항)

### 자신의 도메인 사용하기

1. 도메인 구매 (예: docs.mysite.com)

2. DNS 설정:
   ```
   Type: CNAME
   Name: docs
   Value: miniforce1119.github.io
   ```

3. `agent-builder-automation/docs/` 폴더에 `CNAME` 파일 생성:
   ```
   docs.mysite.com
   ```

4. GitHub Settings → Pages → Custom domain 설정

5. 배포 후 HTTPS 활성화

## 📚 참고 자료

- [GitHub Pages 공식 문서](https://docs.github.com/en/pages)
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [MkDocs gh-deploy 문서](https://www.mkdocs.org/user-guide/deploying-your-docs/)
- [Material for MkDocs 배포 가이드](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)

## ✅ 체크리스트

배포 전 확인사항:

- [ ] `.github/workflows/deploy-docs.yml` 파일 존재
- [ ] `mkdocs.yml`에 `site_url` 설정
- [ ] GitHub Pages 활성화 (Settings → Pages)
- [ ] GitHub Actions 권한 설정 (Read and write)
- [ ] docs 폴더에 `index.md` 파일 존재
- [ ] 테스트 로컬 빌드 성공 (`mkdocs build`)

배포 후 확인사항:

- [ ] GitHub Actions 워크플로우 성공 (녹색 체크)
- [ ] gh-pages 브랜치 생성 확인
- [ ] 사이트 접속 가능 (https://miniforce1119.github.io/Documents/)
- [ ] 네비게이션 정상 작동
- [ ] 검색 기능 작동
- [ ] 다크 모드 전환 작동

---

**배포 준비 완료!** 🚀

이제 코드를 push하면 자동으로 GitHub Pages에 배포됩니다!
