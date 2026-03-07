#!/usr/bin/env python3
"""
테스트용 Agent 출력 파일을 생성하는 스크립트

Usage:
    python create_test_doc.py "문서 제목" [카테고리]
"""

import sys
from datetime import datetime


def create_test_document(title: str, category: str = "analysis"):
    """Create a test document in Agent Builder output format."""
    filename = title.lower().replace(" ", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"""TITLE:
{title}

FILENAME:
{filename}

CONTENT:
# {title}

> 생성일: {timestamp}  
> 카테고리: {category}

## 📋 개요

이것은 자동 생성된 테스트 문서입니다.

## 🎯 목적

이 문서는 Agent Builder를 시뮬레이션하여 생성되었습니다.

## 📝 주요 내용

### 섹션 1
- 항목 1-1
- 항목 1-2
- 항목 1-3

### 섹션 2
- 항목 2-1
- 항목 2-2
- 항목 2-3

### 섹션 3
- 항목 3-1
- 항목 3-2
- 항목 3-3

## 💡 예제 코드

```python
def example():
    print("Hello, World!")
    return True
```

## 📊 데이터 테이블

| 항목 | 값 | 비고 |
|------|-----|------|
| 항목 1 | 100 | 정상 |
| 항목 2 | 200 | 양호 |
| 항목 3 | 300 | 우수 |

## 🔗 참고 링크

- [링크 1](#)
- [링크 2](#)
- [링크 3](#)

## ✅ 결론

테스트 문서 작성이 완료되었습니다.

---

**작성자**: Test Script  
**작성일**: {timestamp}
"""
    
    output_file = f"test_{filename}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 테스트 파일 생성 완료: {output_file}")
    print(f"\n📌 다음 명령어로 실행하세요:")
    print(f"   python export_agent_to_docs.py --input {output_file} --category {category} --dry-run")
    print(f"   python export_agent_to_docs.py --input {output_file} --category {category} --skip-git")
    print(f"   python export_agent_to_docs.py --input {output_file} --category {category}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python create_test_doc.py '문서 제목' [카테고리]")
        print("\n예시:")
        print("  python create_test_doc.py 'Python 베스트 프랙티스'")
        print("  python create_test_doc.py 'API 설계 가이드' guides")
        print("  python create_test_doc.py '데이터 분석 리포트' reports")
        sys.exit(1)
    
    title = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "analysis"
    
    create_test_document(title, category)


if __name__ == "__main__":
    main()
