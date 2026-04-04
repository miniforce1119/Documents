# Slidev + MkDocs GitHub Pages 배포 가이드

> **목적:** Slidev로 만든 프레젠테이션을 MkDocs 문서 사이트와 함께 GitHub Pages에 배포하는 전체 과정을 정리한 가이드입니다.
> Cline 또는 다른 AI 코딩 에이전트에게 이 문서를 전달하면 동일한 환경을 구성할 수 있습니다.

---

## 목차

1. [전체 구조 이해](#1-전체-구조-이해)
2. [사전 준비](#2-사전-준비)
3. [프로젝트 초기 설정](#3-프로젝트-초기-설정)
4. [Slidev 프레젠테이션 작성](#4-slidev-프레젠테이션-작성)
5. [MkDocs 설정](#5-mkdocs-설정)
6. [빌드 및 배포](#6-빌드-및-배포)
7. [배포 자동화 스크립트](#7-배포-자동화-스크립트)
8. [트러블슈팅](#8-트러블슈팅)
9. [Cline 작업 체크리스트](#9-cline-작업-체크리스트)

---

## 1. 전체 구조 이해

### 최종 디렉토리 구조

```
Documents/                          # Git 저장소 루트
├── .git/
├── .gitignore                      # venv/, node_modules/ 등 제외
├── README.md
├── SLIDEV_DEPLOY_GUIDE.md          # 이 문서
├── venv/                           # Python 가상환경 (MkDocs용)
│
├── agent-builder-automation/       # MkDocs 프로젝트
│   ├── mkdocs.yml                  # MkDocs 설정 파일
│   ├── docs/                       # 마크다운 문서 소스
│   │   ├── index.md
│   │   ├── presentations.md        # 슬라이드 링크 목록 페이지
│   │   ├── courses/
│   │   ├── guides/
│   │   ├── analysis/
│   │   └── concepts/
│   └── site/                       # MkDocs 빌드 결과 (gitignore)
│
└── slidev-sample/                  # Slidev 프레젠테이션 프로젝트
    ├── package.json
    ├── slides.md                   # 슬라이드 소스 (핵심 파일)
    ├── style.css                   # 커스텀 스타일 (라이트 모드 강제 등)
    └── dist/                       # Slidev 빌드 결과 (gitignore)
```

### GitHub Pages 배포 후 구조 (gh-pages 브랜치)

```
gh-pages 브랜치 루트
├── index.html                      # MkDocs 메인 페이지
├── concepts/
├── courses/
├── guides/
├── analysis/
├── presentations/                  # 슬라이드 링크 목록
├── search/
├── assets/                         # MkDocs 테마 자산
└── slides/                         # Slidev 빌드 결과
    └── tech-trends/
        ├── index.html              # Slidev SPA 진입점
        ├── assets/                 # JS, CSS, 폰트 (130+ 파일)
        └── 404.html
```

### 핵심 개념

- **MkDocs**: 마크다운(.md) 파일을 정적 문서 사이트로 빌드
- **Slidev**: 마크다운(.md) 파일을 SPA(Single Page Application) 프레젠테이션으로 빌드
- **GitHub Pages**: 정적 파일(HTML, CSS, JS)을 호스팅하는 서비스
- **gh-pages 브랜치**: GitHub Pages가 서빙하는 브랜치. 빌드 결과물만 들어감
- 두 도구의 빌드 결과를 **하나의 site/ 폴더에 합쳐서** gh-pages에 배포

---

## 2. 사전 준비

### 필요한 도구

| 도구 | 용도 | 설치 확인 |
|------|------|-----------|
| Git | 버전 관리 및 배포 | `git --version` |
| Python 3.x | MkDocs 실행 | `python --version` |
| Node.js 18+ | Slidev 실행 | `node --version` |
| npm | Node.js 패키지 관리 | `npm --version` |

### GitHub 저장소 설정

1. GitHub에서 저장소 생성 (예: `Documents`)
2. Settings > Pages > Source: **Deploy from a branch**
3. Branch: **gh-pages** / **/ (root)** 선택
4. Save

---

## 3. 프로젝트 초기 설정

### 3-1. 저장소 클론

```bash
git clone https://github.com/{username}/Documents.git
cd Documents
```

### 3-2. Python 가상환경 + MkDocs 설치

```bash
# 가상환경 생성 (프로젝트 루트에)
python -m venv venv

# 활성화
# Windows Git Bash:
source venv/Scripts/activate
# Mac/Linux:
source venv/bin/activate

# MkDocs + Material 테마 설치
pip install mkdocs mkdocs-material
```

### 3-3. .gitignore 설정

```
venv/
node_modules/
dist/
site/
__pycache__/
```

### 3-4. Slidev 프로젝트 생성

```bash
mkdir slidev-sample
cd slidev-sample
npm init -y
npm install @slidev/cli @slidev/theme-default @slidev/theme-seriph
```

`package.json`의 scripts에 추가:

```json
{
  "scripts": {
    "dev": "slidev",
    "build": "slidev build",
    "export": "slidev export"
  }
}
```

---

## 4. Slidev 프레젠테이션 작성

### 4-1. slides.md 작성

`slidev-sample/slides.md` 파일이 슬라이드의 전부입니다.

```markdown
---
theme: default
title: "프레젠테이션 제목"
colorSchema: light
layout: intro
class: text-center
highlighter: shiki
transition: slide-left
---

# 프레젠테이션 제목

부제목

---

# 슬라이드 2

- 항목 1
- 항목 2
- 항목 3

---
layout: section
---

# 섹션 구분

---

# 코드 예시

```python
print("Hello, World!")
```
```

**주요 규칙:**
- `---`로 슬라이드를 구분
- 첫 번째 `---` 블록은 frontmatter (설정)
- 마크다운 문법 그대로 사용
- Mermaid 다이어그램, KaTeX 수식 지원

### 4-2. 라이트 모드 강제 설정

Slidev는 기본적으로 사용자의 시스템 테마를 따르므로, 다크모드 환경에서는 검은 배경으로 표시됩니다.
**밝은 배경을 강제하려면** `slidev-sample/style.css` 파일을 생성합니다:

```css
:root {
  --slidev-theme-default-background: #ffffff !important;
  --slidev-theme-default-headingColor: #1a1a2e !important;
  color-scheme: light !important;
}

html, body {
  color-scheme: light !important;
}

html.dark {
  --slidev-theme-default-background: #ffffff !important;
  --slidev-theme-default-headingColor: #1a1a2e !important;
  color-scheme: light !important;
}

.dark .slidev-layout {
  background: #ffffff !important;
  color: #1a1a2e !important;
}

.slidev-layout {
  background: #ffffff !important;
  color: #1a1a2e !important;
}

.slidev-layout h1,
.slidev-layout h2,
.slidev-layout h3,
.slidev-layout h4,
.slidev-layout p,
.slidev-layout li,
.slidev-layout td,
.slidev-layout th,
.slidev-layout span,
.slidev-layout div {
  color: #1a1a2e !important;
}

.slidev-layout a {
  color: #2563eb !important;
}

.slidev-layout code {
  color: #1a1a2e !important;
}
```

> Slidev는 프로젝트 루트의 `style.css`를 자동으로 로드합니다.

### 4-3. 배경색이 있는 박스 사용 시 주의

밝은 배경 박스(bg-green-50, bg-blue-50 등)를 사용할 때 반드시 `text-gray-800`을 함께 지정해야 다크모드에서도 텍스트가 보입니다:

```html
<!-- 잘못된 예 - 다크모드에서 글자 안 보임 -->
<div class="p-5 bg-green-50 border border-green-200">
내용
</div>

<!-- 올바른 예 -->
<div class="p-5 bg-green-50 border border-green-200 text-gray-800">
내용
</div>
```

### 4-4. 로컬 미리보기

```bash
cd slidev-sample
npx slidev
# http://localhost:3030 에서 확인
```

---

## 5. MkDocs 설정

### 5-1. mkdocs.yml에 프레젠테이션 탭 추가

`agent-builder-automation/mkdocs.yml`의 `nav` 섹션에 추가:

```yaml
nav:
  - 홈: index.md
  - 강의 자료:
      - AI 기초: courses/ai-fundamentals.md
  - 가이드:
      - Agent Builder: guides/agent-builder.md
  - 분석:
      - 보고서: analysis/report.md
  - 개념:
      - Python: concepts/python.md
  - 프레젠테이션: presentations.md        # 이 줄 추가
```

### 5-2. presentations.md 생성

`agent-builder-automation/docs/presentations.md`:

```markdown
# 프레젠테이션

강의 및 발표에 사용되는 슬라이드 자료입니다.

| 제목 | 설명 | 링크 |
|------|------|------|
| Slidev to GitHub Pages | Slidev 배포 가이드 발표 자료 | [슬라이드 보기](/Documents/slides/tech-trends/) |
```

**링크 형식 주의사항:**
- 절대 경로 사용: `/Documents/slides/{슬라이드명}/`
- 상대 경로(`../../slides/...`)는 MkDocs 빌드 시 경고 발생하지만 동작함
- `{username}.github.io` 뒤의 저장소명이 base path가 됨

---

## 6. 빌드 및 배포

### 6-1. Slidev 빌드

```bash
cd slidev-sample

# Windows Git Bash (MSYS_NO_PATHCONV 필수!)
MSYS_NO_PATHCONV=1 npx slidev build --base /Documents/slides/tech-trends/

# Mac/Linux
npx slidev build --base /Documents/slides/tech-trends/
```

**`--base` 옵션이 핵심입니다:**
- GitHub Pages의 URL 구조에 맞춰야 함
- 형식: `/{저장소명}/slides/{슬라이드명}/`
- 이 값이 틀리면 JS/CSS 로드 실패로 빈 화면 표시

**Windows Git Bash 주의:**
- `MSYS_NO_PATHCONV=1`을 안 붙이면 Git Bash가 `/Documents`를 `C:/Program Files/Git/Documents`로 변환해서 경로가 깨짐
- 이 문제로 한참 고생할 수 있으므로 반드시 붙일 것

### 6-2. MkDocs 빌드

```bash
cd agent-builder-automation
source ../venv/Scripts/activate    # Windows
# source ../venv/bin/activate      # Mac/Linux
mkdocs build
```

### 6-3. Slidev 결과를 MkDocs site에 복사

```bash
mkdir -p site/slides/tech-trends
cp -r ../slidev-sample/dist/* site/slides/tech-trends/
```

### 6-4. gh-pages에 배포

```bash
ghp-import -n -p -f site
```

| 옵션 | 의미 |
|------|------|
| `-n` | `.nojekyll` 파일 추가 (Jekyll 처리 방지) |
| `-p` | push까지 자동 실행 |
| `-f` | 강제 덮어쓰기 |

> `ghp-import`는 MkDocs 설치 시 함께 설치됩니다 (`pip install mkdocs`).

### 왜 `mkdocs gh-deploy` 대신 `ghp-import`을 쓰는가?

`mkdocs gh-deploy --force`는 내부적으로:
1. `mkdocs build` (site/ 재빌드)
2. `ghp-import` (gh-pages에 push)

를 순서대로 실행합니다. 문제는 **1번에서 site/를 다시 빌드하면서 우리가 복사해둔 slides/ 폴더를 날려버립니다.**

그래서 반드시 이 순서를 따라야 합니다:
1. `mkdocs build` (MkDocs 빌드)
2. `cp -r` (Slidev 결과 복사)
3. `ghp-import -n -p -f site` (배포만 실행)

---

## 7. 배포 자동화 스크립트

매번 명령어를 하나씩 치기 귀찮으므로 스크립트를 만들어 사용합니다.

### deploy.sh (Windows Git Bash)

```bash
#!/bin/bash
# deploy.sh - MkDocs + Slidev 통합 배포 스크립트

set -e  # 에러 발생 시 중단

REPO_DIR="/c/project/Documents"
SLIDEV_DIR="$REPO_DIR/slidev-sample"
MKDOCS_DIR="$REPO_DIR/agent-builder-automation"
SLIDES_BASE="/Documents/slides/tech-trends/"

echo "=== 1/4 Slidev 빌드 ==="
cd "$SLIDEV_DIR"
MSYS_NO_PATHCONV=1 npx slidev build --base "$SLIDES_BASE"

echo "=== 2/4 MkDocs 빌드 ==="
cd "$MKDOCS_DIR"
source ../venv/Scripts/activate
mkdocs build

echo "=== 3/4 Slidev 결과 복사 ==="
mkdir -p site/slides/tech-trends
cp -r "$SLIDEV_DIR/dist/"* site/slides/tech-trends/

echo "=== 4/4 gh-pages 배포 ==="
ghp-import -n -p -f site

echo "=== 배포 완료! ==="
echo "문서: https://{username}.github.io/Documents/"
echo "슬라이드: https://{username}.github.io/Documents/slides/tech-trends/"
```

### 사용법

```bash
chmod +x deploy.sh
./deploy.sh
```

### deploy.sh (Mac/Linux)

Windows 버전과 거의 동일하되, 두 가지만 변경:

```bash
# 경로 변경
REPO_DIR="$HOME/project/Documents"

# venv 활성화 변경
source ../venv/bin/activate

# MSYS_NO_PATHCONV 불필요
npx slidev build --base "$SLIDES_BASE"
```

---

## 8. 트러블슈팅

### 빈 화면 / 404 Page not found

**원인:** `--base` 경로가 잘못됨

**확인 방법:**
```bash
# 빌드된 index.html에서 경로 확인
head -20 slidev-sample/dist/index.html
```

`src="/Documents/slides/tech-trends/assets/..."`처럼 올바른 경로가 들어있어야 합니다.

**잘못된 예시 (Windows Git Bash):**
```
src="/Program Files/Git/Documents/slides/tech-trends/assets/..."
```
이 경우 `MSYS_NO_PATHCONV=1`을 빠뜨린 것입니다.

### slides/ 폴더가 gh-pages에 없음

**원인:** `mkdocs gh-deploy`를 사용해서 site/가 재빌드됨

**해결:** `mkdocs gh-deploy` 대신 `ghp-import -n -p -f site` 사용

### 다크모드에서 박스 안 텍스트 안 보임

**원인:** 밝은 배경 박스에 텍스트 색상 미지정

**해결:** `text-gray-800` 클래스 추가 또는 `style.css`로 전역 라이트 모드 강제

### ghp-import 명령을 찾을 수 없음

**원인:** Python 가상환경이 활성화 안 됨

**해결:**
```bash
source venv/Scripts/activate    # Windows
source venv/bin/activate        # Mac/Linux
```

### MkDocs 빌드 시 presentations.md 링크 경고

```
INFO - Doc file 'presentations.md' contains an absolute link '/Documents/slides/tech-trends/', it was left as is.
```

이 경고는 **무시해도 됩니다.** MkDocs가 관리하지 않는 외부 경로이므로 경고를 보여주지만 동작에 문제없습니다.

---

## 9. Cline 작업 체크리스트

Cline에게 작업을 시킬 때 아래 체크리스트를 함께 전달하세요.

### 초기 설정

- [ ] 저장소 클론
- [ ] Python venv 생성 및 mkdocs, mkdocs-material 설치
- [ ] .gitignore에 venv/, node_modules/, dist/, site/ 추가
- [ ] slidev-sample/ 폴더 생성 및 npm 패키지 설치
- [ ] slides.md 작성
- [ ] style.css 생성 (라이트 모드 강제)

### MkDocs 연동

- [ ] mkdocs.yml nav에 "프레젠테이션" 탭 추가
- [ ] docs/presentations.md 생성 (슬라이드 링크 목록)

### 빌드 및 배포

- [ ] Slidev 빌드 (`MSYS_NO_PATHCONV=1 npx slidev build --base /Documents/slides/{이름}/`)
- [ ] index.html에서 경로 확인 (head -20 dist/index.html)
- [ ] MkDocs 빌드 (`mkdocs build`)
- [ ] Slidev 결과를 site/slides/{이름}/에 복사
- [ ] `ghp-import -n -p -f site`로 배포 (**mkdocs gh-deploy 사용 금지**)
- [ ] GitHub Pages에서 확인

### 새 슬라이드 추가 시

- [ ] slidev-sample/slides.md 수정 또는 새 Slidev 프로젝트 생성
- [ ] 새 슬라이드의 --base 경로 결정
- [ ] presentations.md에 링크 추가
- [ ] deploy.sh 스크립트에 새 슬라이드 빌드/복사 단계 추가
- [ ] 배포 및 확인

---

## 참고 링크

| 항목 | URL |
|------|-----|
| Slidev 공식 문서 | https://sli.dev |
| MkDocs 공식 문서 | https://www.mkdocs.org |
| Material for MkDocs | https://squidfunk.github.io/mkdocs-material |
| ghp-import | https://github.com/c-w/ghp-import |
| 현재 배포된 문서 | https://miniforce1119.github.io/Documents/ |
| 현재 배포된 슬라이드 | https://miniforce1119.github.io/Documents/slides/tech-trends/ |

---

*마지막 업데이트: 2026-04-04*
