# AI와 함께 나만의 문서 사이트 만들기

> **바이브 코딩으로 MkDocs + GitHub Pages 구축하기**
>
> 이 가이드는 코딩 경험이 없어도 AI에게 물어보면서 따라할 수 있도록 만들었습니다.
> 강의에서 본 시연을 집에서 직접 해볼 수 있습니다.

---

## 이 가이드의 목표

| 항목 | 내용 |
|------|------|
| **만들 것** | 나만의 문서 웹사이트 |
| **사용 도구** | MkDocs (문서 사이트 생성기) + GitHub Pages (무료 호스팅) |
| **핵심 방법** | AI에게 물어보면서 만든다 (바이브 코딩) |
| **소요 시간** | 약 1~2시간 |
| **필요 경험** | 없음 (처음부터 안내합니다) |

### 완성하면 이런 사이트가 만들어집니다

```
https://내아이디.github.io/my-docs/
```

누구나 접속할 수 있는 나만의 문서 사이트가 인터넷에 공개됩니다.

---

## 바이브 코딩이란?

바이브 코딩은 **AI에게 자연어로 설명하면 AI가 코드를 만들어주는** 방식입니다.

```
나: "Python으로 MkDocs 설치하는 명령어 알려줘"
AI: "pip install mkdocs mkdocs-material 을 터미널에 입력하세요"
나: (복사해서 붙여넣기)
```

코드를 외울 필요 없습니다. **AI에게 물어보고, 복사하고, 붙여넣기** 하면 됩니다.

---

## Part 0: 사전 준비

집에서 시작하기 전에 아래 4가지를 설치합니다.
이것도 AI에게 물어보면서 하면 됩니다.

### 0-1. Git 설치

Git은 파일의 변경 이력을 관리하는 도구입니다.

1. https://git-scm.com 접속
2. **Download for Windows** 클릭
3. 설치 파일 실행 -> **모두 기본값(Next)** 으로 설치

!!! tip "설치 확인"

    설치 후 **시작 메뉴**에서 `Git Bash`를 검색해서 열고, 아래를 입력합니다:
    ```bash
    git --version
    ```
    `git version 2.xx.x` 같은 결과가 나오면 성공입니다.

### 0-2. Python 설치

Python은 MkDocs를 실행하는 데 필요한 프로그래밍 언어입니다.

1. https://www.python.org 접속
2. **Downloads** -> **Download Python 3.x.x** 클릭
3. 설치 시 **반드시** `Add Python to PATH` 체크 후 Install

!!! warning "중요: Add Python to PATH"

    설치 화면 맨 아래에 `Add Python to PATH` 체크박스가 있습니다.
    **반드시 체크**해야 합니다. 체크하지 않으면 이후 명령어가 동작하지 않습니다.

!!! tip "설치 확인"

    Git Bash에서:
    ```bash
    python --version
    ```
    `Python 3.x.x` 같은 결과가 나오면 성공입니다.

### 0-3. VS Code 설치

VS Code는 파일을 편집하는 도구입니다. 메모장의 상위 버전이라고 생각하면 됩니다.

1. https://code.visualstudio.com 접속
2. **Download for Windows** 클릭
3. 설치 파일 실행 -> 기본값으로 설치

### 0-4. GitHub 계정 만들기

GitHub는 코드를 저장하고 웹사이트를 무료로 호스팅해주는 서비스입니다.

1. https://github.com 접속
2. **Sign up** 클릭
3. 이메일, 비밀번호, 사용자이름 입력하여 가입

!!! note "사용자이름이 곧 사이트 주소"

    GitHub 사용자이름이 `hong` 이면 사이트 주소는 `https://hong.github.io/...`가 됩니다.
    기억하기 쉬운 이름을 추천합니다.

---

## Part 1: 프로젝트 만들기

이제부터 본격적으로 시작합니다.
**Git Bash** 를 열어주세요 (시작 메뉴에서 검색).

### 1-1. 작업 폴더 만들기

아래 명령어를 Git Bash에 한 줄씩 복사해서 붙여넣으세요.

```bash
cd ~
mkdir my-docs
cd my-docs
```

| 명령어 | 의미 |
|--------|------|
| `cd ~` | 내 홈 폴더로 이동 |
| `mkdir my-docs` | `my-docs` 폴더 생성 |
| `cd my-docs` | 그 폴더로 이동 |

### 1-2. MkDocs 설치

```bash
pip install mkdocs mkdocs-material
```

이 한 줄이면 MkDocs와 예쁜 테마(Material)가 설치됩니다.
설치에 1~2분 정도 걸릴 수 있습니다.

### 1-3. MkDocs 프로젝트 생성

```bash
mkdocs new .
```

`.` 은 "현재 폴더에 만들어라" 라는 뜻입니다.

이 명령을 실행하면 아래 파일들이 자동으로 만들어집니다:

```
my-docs/
├── mkdocs.yml          <- 사이트 설정 파일
└── docs/
    └── index.md        <- 첫 페이지
```

---

## Part 2: AI에게 설정 파일 만들어달라고 하기

여기서부터가 **바이브 코딩**의 핵심입니다.

### 2-1. AI에게 요청하기

ChatGPT나 Claude에 아래 프롬프트를 복사해서 붙여넣으세요:

!!! example "AI에게 보낼 프롬프트"

    ```
    MkDocs Material 테마로 기술 문서 사이트를 만들고 있어.
    아래 조건에 맞는 mkdocs.yml 파일 내용을 만들어줘.

    조건:
    - 사이트 이름: "내 기술 노트"
    - 한국어 검색 지원
    - 다크모드/라이트모드 전환 가능
    - 코드 복사 버튼 활성화
    - 네비게이션 탭 사용
    - nav 구조:
      - 홈: index.md
      - 가이드:
        - 시작하기: guides/getting-started.md
      - 메모:
        - 첫 번째 메모: notes/first-note.md
    ```

### 2-2. AI의 답변을 파일에 적용하기

AI가 `mkdocs.yml` 내용을 알려주면:

1. VS Code를 실행합니다
2. **File** -> **Open Folder** -> `my-docs` 폴더 선택
3. 왼쪽 파일 목록에서 `mkdocs.yml` 클릭
4. 기존 내용을 **전부 지우고** AI가 준 내용을 **붙여넣기**
5. ++ctrl+s++ 로 저장

!!! tip "AI 답변 예시"

    AI가 이런 식으로 답변할 것입니다 (그대로 사용하셔도 됩니다):
    ```yaml
    site_name: 내 기술 노트
    site_description: 개인 기술 문서 사이트
    site_url: https://내아이디.github.io/my-docs/

    theme:
      name: material
      language: ko
      palette:
        - scheme: default
          primary: indigo
          accent: indigo
          toggle:
            icon: material/brightness-7
            name: 다크 모드로 전환
        - scheme: slate
          primary: indigo
          accent: indigo
          toggle:
            icon: material/brightness-4
            name: 라이트 모드로 전환
      features:
        - navigation.tabs
        - navigation.sections
        - navigation.top
        - search.suggest
        - search.highlight
        - content.code.copy

    plugins:
      - search:
          lang:
            - ko
            - en

    markdown_extensions:
      - pymdownx.highlight:
          anchor_linenums: true
      - pymdownx.inlinehilite
      - pymdownx.superfences
      - pymdownx.tabbed:
          alternate_style: true
      - admonition
      - pymdownx.details
      - attr_list
      - tables

    nav:
      - 홈: index.md
      - 가이드:
          - 시작하기: guides/getting-started.md
      - 메모:
          - 첫 번째 메모: notes/first-note.md
    ```

### 2-3. 문서 파일 만들기

`nav`에 적은 파일들을 실제로 만들어야 합니다.

Git Bash에서:

```bash
mkdir -p docs/guides
mkdir -p docs/notes
```

그리고 AI에게 내용도 만들어달라고 합니다:

!!! example "AI에게 보낼 프롬프트"

    ```
    MkDocs용 마크다운 파일 3개를 만들어줘.

    1. docs/index.md - 사이트 홈페이지. 환영 인사와 사이트 소개.
    2. docs/guides/getting-started.md - MkDocs 시작 가이드 간단 요약.
    3. docs/notes/first-note.md - 오늘 배운 바이브 코딩에 대한 메모.

    각 파일마다 제목, 소개, 목차가 포함되게 해줘.
    마크다운 형식으로 작성해줘.
    ```

AI가 만들어준 내용을 각 파일에 복사하여 저장합니다.

!!! tip "VS Code에서 새 파일 만들기"

    1. 왼쪽 파일 탐색기에서 `docs` 폴더 우클릭
    2. **New File** 클릭
    3. 파일명 입력 (예: `guides/getting-started.md`)
    4. AI가 준 내용 붙여넣기
    5. ++ctrl+s++ 저장

---

## Part 3: 내 컴퓨터에서 미리보기

문서를 인터넷에 올리기 전에 내 컴퓨터에서 먼저 확인합니다.

### 3-1. 로컬 서버 실행

Git Bash에서:

```bash
mkdocs serve
```

이 명령을 실행하면 아래와 같은 메시지가 나옵니다:

```
INFO    -  Serving on http://127.0.0.1:8000/
```

### 3-2. 브라우저에서 확인

웹 브라우저(Chrome 등)를 열고 주소창에 입력:

```
http://127.0.0.1:8000
```

내가 만든 문서 사이트가 보이면 성공입니다!

!!! tip "실시간 반영"

    `mkdocs serve`가 실행 중인 상태에서 마크다운 파일을 수정하고 저장하면,
    브라우저를 새로고침하지 않아도 **자동으로 변경사항이 반영**됩니다.

!!! tip "서버 종료"

    Git Bash에서 ++ctrl+c++ 를 누르면 서버가 종료됩니다.

---

## Part 4: GitHub에 올리기

이제 만든 사이트를 인터넷에 공개할 차례입니다.

### 4-1. GitHub에 저장소 만들기

1. https://github.com 에 로그인
2. 오른쪽 상단 `+` 버튼 -> **New repository** 클릭
3. 아래와 같이 설정:

| 항목 | 입력값 |
|------|--------|
| Repository name | `my-docs` |
| Description | 내 기술 노트 (선택사항) |
| Public / Private | **Public** 선택 |
| Initialize this repository | **체크하지 않음** |

4. **Create repository** 클릭

### 4-2. 내 컴퓨터와 GitHub 연결하기

GitHub에서 저장소를 만들면 안내 화면이 나옵니다.
Git Bash에서 아래 명령어를 **한 줄씩** 실행합니다:

```bash
git init
git add .
git commit -m "첫 번째 커밋: MkDocs 프로젝트 생성"
git branch -M main
git remote add origin https://github.com/내아이디/my-docs.git
git push -u origin main
```

!!! warning "내아이디 부분 수정"

    `내아이디` 부분을 본인의 GitHub 사용자이름으로 바꿔야 합니다.
    예: `https://github.com/hong/my-docs.git`

!!! note "처음 push할 때"

    처음 push하면 GitHub 로그인 창이 뜰 수 있습니다.
    GitHub 아이디와 비밀번호(또는 Personal Access Token)를 입력하면 됩니다.

---

## Part 5: GitHub Pages로 자동 배포 설정하기

GitHub에 코드를 올릴 때마다 자동으로 사이트가 업데이트되도록 설정합니다.

### 5-1. AI에게 GitHub Actions 설정 파일 만들어달라고 하기

!!! example "AI에게 보낼 프롬프트"

    ```
    GitHub Actions로 MkDocs를 자동 배포하는 워크플로우 파일을 만들어줘.

    조건:
    - main 브랜치에 push하면 자동 실행
    - Python 3.12 사용
    - mkdocs, mkdocs-material 설치
    - mkdocs gh-deploy --force 로 배포
    - 파일 경로: .github/workflows/deploy.yml
    ```

### 5-2. 워크플로우 파일 만들기

Git Bash에서 폴더를 만들고:

```bash
mkdir -p .github/workflows
```

VS Code에서 `.github/workflows/deploy.yml` 파일을 만들고 AI가 준 내용을 붙여넣습니다.

!!! tip "AI 답변 예시"

    이런 내용이 나올 것입니다 (그대로 사용 가능):
    ```yaml
    name: Deploy MkDocs

    on:
      push:
        branches:
          - main

    permissions:
      contents: write

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Setup Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.12'

          - name: Install dependencies
            run: pip install mkdocs mkdocs-material

          - name: Deploy
            run: mkdocs gh-deploy --force
    ```

### 5-3. 배포 설정 파일을 GitHub에 올리기

```bash
git add .
git commit -m "GitHub Actions 자동 배포 설정 추가"
git push
```

### 5-4. GitHub Pages 활성화

1. GitHub에서 `my-docs` 저장소 페이지로 이동
2. **Settings** 탭 클릭 (상단 메뉴)
3. 왼쪽 메뉴에서 **Pages** 클릭
4. Source 항목에서:
    - **Deploy from a branch** 선택
    - Branch: **gh-pages** / **/ (root)** 선택
    - **Save** 클릭

!!! note "gh-pages 브랜치가 안 보이면?"

    첫 push 후 GitHub Actions가 실행되어야 gh-pages 브랜치가 생깁니다.
    GitHub 저장소의 **Actions** 탭에서 워크플로우 실행이 완료될 때까지 1~2분 기다린 후
    다시 Settings -> Pages 에서 확인하세요.

### 5-5. 사이트 확인

1~2분 후 아래 주소로 접속합니다:

```
https://내아이디.github.io/my-docs/
```

내가 만든 문서 사이트가 전 세계에 공개된 것입니다!

---

## Part 6: 문서 추가하고 업데이트하기

사이트는 한번 만들고 끝이 아닙니다.
새 문서를 추가하고 싶을 때 이 과정을 반복하면 됩니다.

### 6-1. AI에게 새 문서 만들어달라고 하기

!!! example "AI에게 보낼 프롬프트 예시"

    ```
    MkDocs용 마크다운 문서를 만들어줘.

    주제: Python 기초 문법 정리
    파일 위치: docs/notes/python-basics.md
    포함할 내용: 변수, 조건문, 반복문, 함수 기초
    ```

### 6-2. mkdocs.yml 수정

새 문서를 추가했으면 `mkdocs.yml`의 `nav` 부분에도 추가합니다:

```yaml
nav:
  - 홈: index.md
  - 가이드:
      - 시작하기: guides/getting-started.md
  - 메모:
      - 첫 번째 메모: notes/first-note.md
      - Python 기초: notes/python-basics.md      # <- 이 줄 추가
```

### 6-3. GitHub에 올리기

```bash
git add .
git commit -m "Python 기초 문서 추가"
git push
```

push하면 GitHub Actions가 자동으로 실행되어 1~2분 후 사이트에 반영됩니다.

---

## Part 7: 바이브 코딩 활용 팁

### 이런 것도 AI에게 요청할 수 있습니다

| 요청 | 프롬프트 예시 |
|------|---------------|
| 회의록 템플릿 | "MkDocs용 주간 회의록 마크다운 템플릿 만들어줘" |
| 업무 매뉴얼 | "신입사원용 장비 세팅 가이드를 마크다운으로 만들어줘" |
| 트러블슈팅 문서 | "자주 발생하는 HW 이슈 FAQ 문서를 마크다운 표 형태로 만들어줘" |
| 사이트 꾸미기 | "mkdocs.yml에 로고, 파비콘, 소셜 링크 추가하는 방법 알려줘" |
| 오류 해결 | "(에러 메시지 복사) 이 에러 어떻게 해결해?" |

### 바이브 코딩 3단계 공식

```
1. AI에게 물어본다    -> "이런 거 만들어줘"
2. 결과를 복사한다    -> AI 답변에서 코드/내용 복사
3. 파일에 붙여넣는다  -> VS Code에서 저장
```

이것을 반복하면 어떤 문서 사이트든 만들 수 있습니다.

---

## 부록 A: 마크다운 기본 문법

마크다운은 텍스트에 간단한 기호를 붙여서 서식을 지정하는 방법입니다.

```markdown
# 제목 1 (가장 큰 제목)
## 제목 2
### 제목 3

**굵은 글씨**
*기울임 글씨*

- 목록 항목 1
- 목록 항목 2
  - 하위 항목

1. 번호 목록 1
2. 번호 목록 2

> 인용문

| 열1 | 열2 | 열3 |
|-----|-----|-----|
| A   | B   | C   |

[링크 텍스트](https://example.com)
```

!!! tip "마크다운을 몰라도 괜찮습니다"

    AI에게 "마크다운 형식으로 만들어줘"라고 하면 알아서 만들어줍니다.

---

## 부록 B: 자주 발생하는 문제와 해결법

### "pip 명령을 찾을 수 없습니다"

**원인:** Python 설치 시 `Add Python to PATH`를 체크하지 않았습니다.

**해결:**

1. Python을 제거합니다 (제어판 -> 프로그램 제거)
2. 다시 설치하면서 `Add Python to PATH` 체크
3. Git Bash를 **닫았다가 다시 열기**

### "git push 시 인증 실패"

**원인:** GitHub 인증이 필요합니다.

**해결:** AI에게 물어보세요:

```
GitHub Personal Access Token 만드는 방법 알려줘.
Windows Git Bash에서 사용하는 방법도 알려줘.
```

### "mkdocs serve 시 에러"

**원인:** `mkdocs.yml` 파일에 문법 오류가 있을 수 있습니다.

**해결:** 에러 메시지를 통째로 복사해서 AI에게 물어보세요:

```
mkdocs serve 실행했는데 이런 에러가 나와:
(에러 메시지 붙여넣기)
어떻게 해결해?
```

### "gh-pages 브랜치가 없습니다"

**원인:** GitHub Actions가 아직 실행되지 않았거나 실패했습니다.

**해결:**

1. GitHub 저장소 -> **Actions** 탭 확인
2. 실패한 워크플로우가 있으면 클릭해서 에러 확인
3. 에러 메시지를 AI에게 물어보기

---

## 부록 C: 전체 명령어 요약 (치트시트)

한눈에 보는 전체 과정입니다:

```bash
# === 최초 1회: 설치 ===
pip install mkdocs mkdocs-material

# === 프로젝트 생성 ===
mkdir my-docs && cd my-docs
mkdocs new .

# === (mkdocs.yml 편집, docs/ 아래 마크다운 파일 작성) ===

# === 로컬 미리보기 ===
mkdocs serve
# 브라우저에서 http://127.0.0.1:8000 접속
# 확인 후 Ctrl+C로 종료

# === GitHub에 올리기 (최초 1회) ===
git init
git add .
git commit -m "첫 번째 커밋"
git branch -M main
git remote add origin https://github.com/내아이디/my-docs.git
git push -u origin main

# === 이후 문서 추가/수정할 때마다 ===
git add .
git commit -m "문서 업데이트"
git push
```

---

## 부록 D: 다음 단계

이 가이드를 완료했다면, 이런 것도 시도해보세요:

- **팀 문서 사이트 만들기** -- 팀원들과 함께 문서를 관리
- **업무 매뉴얼 정리** -- 반복되는 업무 절차를 문서화
- **기술 블로그 운영** -- MkDocs의 블로그 플러그인 활용
- **Slidev로 프레젠테이션 만들기** -- 마크다운으로 슬라이드 제작

무엇이든 AI에게 물어보면서 시작할 수 있습니다.

---

*이 가이드는 바이브 코딩 강의 자료입니다.*
