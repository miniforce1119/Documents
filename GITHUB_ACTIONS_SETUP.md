# GitHub Actions 자동 배포 설정 가이드

## 📌 요약

**GitHub Pages는 현재 정상 작동 중입니다!**
- ✅ 사이트 URL: https://miniforce1119.github.io/Documents/
- ✅ 배포 방식: 수동 배포 (`mkdocs gh-deploy`)

**자동화를 원한다면:** GitHub 웹에서 워크플로우 파일을 직접 생성해야 합니다.

---

## 🔄 현재 배포 방식

### Streamlit에서 Publish 후:

```bash
cd /home/user/webapp/agent-builder-automation
mkdocs gh-deploy --force
```

이 명령만 실행하면 **즉시 GitHub Pages가 업데이트**됩니다!

---

## ⚙️ 자동화 설정 (선택사항)

GitHub Actions로 완전 자동화하려면:

### 1️⃣ GitHub 웹에서 파일 생성

1. https://github.com/miniforce1119/Documents 접속
2. **"Add file" → "Create new file"**
3. 파일명: `.github/workflows/deploy-docs.yml`
4. 아래 내용 붙여넣기:

```yaml
name: Deploy MkDocs

on:
  push:
    branches: [main]
    paths:
      - 'agent-builder-automation/docs/**'
      - 'agent-builder-automation/mkdocs.yml'

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install mkdocs mkdocs-material
      - run: |
          cd agent-builder-automation
          mkdocs gh-deploy --force
```

5. **Commit** 클릭

### 2️⃣ 자동화 확인

- https://github.com/miniforce1119/Documents/actions
- 워크플로우가 실행되는지 확인

---

## 🎯 최종 워크플로우

### 현재 (수동):
```
1. Streamlit Publish ✅
2. Git push ✅
3. mkdocs gh-deploy 실행 (수동)
4. GitHub Pages 업데이트 ✅
```

### 자동화 후:
```
1. Streamlit Publish ✅
2. Git push ✅
3. GitHub Actions 트리거 (자동)
4. GitHub Pages 업데이트 (자동) ✅
```

---

## 🔗 링크

- **GitHub Pages:** https://miniforce1119.github.io/Documents/
- **GitHub 저장소:** https://github.com/miniforce1119/Documents
- **Streamlit 앱:** https://8501-i395tla92yet3fwt6gb1m-5185f4aa.sandbox.novita.ai
- **MkDocs 로컬:** https://8000-i395tla92yet3fwt6gb1m-5185f4aa.sandbox.novita.ai/Documents/
