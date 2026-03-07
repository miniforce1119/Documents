# 사외 환경 테스트 가이드

## 🎯 목적

회사 Agent Builder 없이 사외 환경에서 MkDocs 문서 자동화 workflow를 테스트하는 방법

## 📋 전제 조건

- Python 3.10+
- Git
- MkDocs (선택사항)

## 🔧 방법 1: 수동 테스트 파일 생성 (추천)

### 1-1. 테스트 파일 생성

로컬 PC에서 `test_agent_output.txt` 파일을 만듭니다:

```txt
TITLE:
나의 첫 번째 테스트 문서

FILENAME:
my-first-test-document

CONTENT:
# 나의 첫 번째 테스트 문서

## 소개

이것은 Agent Builder를 시뮬레이션한 테스트 문서입니다.

## 내용

- 항목 1
- 항목 2
- 항목 3

## 결론

테스트 성공!
```

### 1-2. 스크립트 실행

```bash
# Dry-run으로 먼저 테스트
python export_agent_to_docs.py --input test_agent_output.txt --category analysis --dry-run

# 실제 저장 (git 제외)
python export_agent_to_docs.py --input test_agent_output.txt --category analysis --skip-git

# 전체 workflow 실행 (git 포함)
python export_agent_to_docs.py --input test_agent_output.txt --category analysis
```

## 🤖 방법 2: ChatGPT/Claude 활용

### 2-1. AI에게 요청

ChatGPT나 Claude에게 다음과 같이 요청하세요:

```
다음 주제에 대한 기술 문서를 작성해주세요:
- 주제: [원하는 주제]
- 형식: 아래 포맷으로 작성

TITLE:
[문서 제목]

FILENAME:
[파일명-kebab-case]

CONTENT:
# [문서 제목]

[Markdown 형식의 본문 내용...]
```

### 2-2. 결과 저장

AI가 생성한 결과를 복사해서 `agent_output.txt` 파일로 저장합니다.

### 2-3. 스크립트 실행

```bash
python export_agent_to_docs.py --input agent_output.txt --category guides
```

## 🔄 방법 3: 템플릿 생성기 활용

### 3-1. 템플릿 생성 스크립트

`create_test_doc.py` 파일을 만듭니다:

```python
#!/usr/bin/env python3
import sys

def create_test_document(title: str, category: str = "analysis"):
    filename = title.lower().replace(" ", "-")
    
    content = f"""TITLE:
{title}

FILENAME:
{filename}

CONTENT:
# {title}

## 개요

이것은 자동 생성된 테스트 문서입니다.

## 목차

- 섹션 1
- 섹션 2
- 섹션 3

## 상세 내용

여기에 내용을 추가하세요...

## 결론

문서 작성 완료.
"""
    
    output_file = f"test_{filename}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 테스트 파일 생성: {output_file}")
    print(f"실행: python export_agent_to_docs.py --input {output_file} --category {category}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_test_doc.py '문서 제목' [카테고리]")
        sys.exit(1)
    
    title = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "analysis"
    create_test_document(title, category)
```

### 3-2. 사용 예시

```bash
python create_test_doc.py "Python 베스트 프랙티스" guides
python export_agent_to_docs.py --input test_python-베스트-프랙티스.txt --category guides
```

## 📝 방법 4: 클립보드 활용 (확장)

### 4-1. 클립보드 지원 추가

`export_agent_to_docs.py`에 클립보드 기능을 추가하려면:

```bash
pip install pyperclip
```

### 4-2. 사용 방법

1. ChatGPT/Claude에서 결과 복사
2. 스크립트 실행:
```bash
python export_agent_to_docs.py --from-clipboard --category analysis
```

## 🧪 테스트 시나리오

### 기본 테스트

```bash
# 1. Dry-run 테스트
python export_agent_to_docs.py --input test.txt --dry-run

# 2. 파일만 저장 (git 제외)
python export_agent_to_docs.py --input test.txt --skip-git

# 3. 덮어쓰기 테스트
python export_agent_to_docs.py --input test.txt --overwrite --skip-git

# 4. 다른 카테고리
python export_agent_to_docs.py --input test.txt --category guides --skip-git
```

### MkDocs 연동 테스트

```bash
# 1. Build만
python export_agent_to_docs.py --input test.txt --build --skip-git

# 2. Serve (미리보기)
python export_agent_to_docs.py --input test.txt --serve --skip-git
```

### Git 연동 테스트

```bash
# 전체 workflow
python export_agent_to_docs.py --input test.txt --category analysis
```

## 🎨 다양한 테스트 케이스

### 테스트 케이스 1: 코드 포함 문서

```txt
TITLE:
Python 코드 예제 모음

FILENAME:
python-code-examples

CONTENT:
# Python 코드 예제 모음

## Hello World

```python
def hello():
    print("Hello, World!")

hello()
```

## 클래스 예제

```python
class MyClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"
```
```

### 테스트 케이스 2: 다국어 문서

```txt
TITLE:
多言語ドキュメント / Multilingual Document

FILENAME:
multilingual-document

CONTENT:
# 다국어 문서 예제

## 한국어
안녕하세요!

## English
Hello!

## 日本語
こんにちは！
```

### 테스트 케이스 3: 테이블 포함 문서

```txt
TITLE:
데이터 분석 리포트

FILENAME:
data-analysis-report

CONTENT:
# 데이터 분석 리포트

## 결과 요약

| 항목 | 값 | 비고 |
|------|-----|------|
| 평균 | 85.5 | 양호 |
| 중앙값 | 82.0 | 안정 |
| 표준편차 | 12.3 | 보통 |
```

## 🚀 실전 활용 팁

### Tip 1: 배치 처리

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

### Tip 2: Watch 모드

파일 변경 감지하여 자동 실행:

```bash
# watchdog 설치
pip install watchdog

# 파일 변경 감지
watchmedo shell-command \
    --patterns="*.txt" \
    --command='python export_agent_to_docs.py --input ${watch_src_path} --skip-git' \
    .
```

### Tip 3: 로그 파일 생성

```bash
python export_agent_to_docs.py --input test.txt 2>&1 | tee -a import.log
```

## ✅ 검증 체크리스트

- [ ] 파일이 올바른 경로에 저장되는가?
- [ ] Markdown 포맷이 제대로 보존되는가?
- [ ] Git commit/push가 정상 동작하는가?
- [ ] 한글 파일명이 올바르게 sanitize되는가?
- [ ] 중복 파일명 처리가 되는가?
- [ ] MkDocs build가 정상 동작하는가?

## 🔍 문제 해결

### 문제: 파일명 sanitize 에러

```bash
# 파일명에 특수문자가 너무 많은 경우
# FILENAME에서 영문/숫자/하이픈만 사용하세요
```

### 문제: Git push 실패

```bash
# 인증 확인
git config --list | grep user

# 토큰 재설정
git remote set-url origin https://TOKEN@github.com/USER/REPO.git
```

### 문제: MkDocs 미설치

```bash
pip install mkdocs mkdocs-material
```

## 📦 완전한 테스트 환경 구축

### 1. 의존성 설치

```bash
pip install mkdocs mkdocs-material pyperclip watchdog
```

### 2. 저장소 초기화

```bash
git init
git remote add origin https://github.com/USER/REPO.git
```

### 3. MkDocs 설정

```yaml
# mkdocs.yml
site_name: My Documentation
theme:
  name: material

nav:
  - Home: index.md
  - Analysis: analysis/
  - Guides: guides/
  - Reports: reports/
```

### 4. 첫 테스트 실행

```bash
python export_agent_to_docs.py --input test_agent_output.txt --category analysis --dry-run
python export_agent_to_docs.py --input test_agent_output.txt --category analysis --skip-git
```

## 🎓 다음 단계

1. **클립보드 지원 추가**
2. **Web UI 개발** (Streamlit/Gradio)
3. **GitHub Actions 연동**
4. **자동 목차 생성**
5. **문서 품질 검사**

## 📚 참고 자료

- [MkDocs 공식 문서](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Python argparse](https://docs.python.org/3/library/argparse.html)
