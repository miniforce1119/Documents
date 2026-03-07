# Cline TODO: 사내 AI Agent 연결 가이드

## 📋 개요

이 문서는 회사에서 Cline과 함께 작업할 때 필요한 사내 AI Agent 연결 작업을 정리한 것입니다.

현재 시스템은 **Mock 기반 2-Mode**로 구현되어 있으며, 사내 환경에서는 **실제 Reformat Agent API**로 교체해야 합니다.

---

## 🎯 목표

**외부 AI 결과 → 사내 Reformat Agent → 표준 문서 포맷 변환**

---

## 📂 수정할 파일

### **파일 위치**
```
agent-builder-automation/doc_review_app.py
```

### **수정할 함수**
```python
def reformat_external_text(text: str) -> tuple[str, str, str]:
```

**위치:** 약 60번째 줄 근처

---

## 🔧 작업 내용

### **현재 상태 (Mock)**

```python
def reformat_external_text(text: str) -> tuple[str, str, str]:
    """
    외부 AI 텍스트를 표준 Markdown 문서로 재구성 (Mode B)
    
    TODO (for Cline at company):
    이 함수를 사내 Reformat Agent API로 교체
    """
    # Mock implementation for testing
    lines = text.strip().split('\n')
    
    # 제목 추출 (첫 줄 또는 # 헤더)
    title = lines[0].strip('#').strip() if lines else "Untitled Document"
    
    # 파일명 생성
    filename = sanitize_filename(title)
    
    # Markdown 변환 (규칙 기반 간단한 변환)
    content = f"# {title}\n\n"
    content += f"> 생성일: {datetime.now().strftime('%Y-%m-%d')}\n"
    # ... 나머지 Mock 로직
    
    return (title, filename, content)
```

---

### **변경 후 (사내 API 연동)**

```python
def reformat_external_text(text: str) -> tuple[str, str, str]:
    """
    외부 AI 텍스트를 사내 Reformat Agent를 통해 표준 문서로 재구성
    """
    import requests
    import os
    
    # 환경 변수에서 API 정보 로드
    AGENT_API_URL = os.getenv("AGENT_REFORMAT_URL", "https://agent-builder.company.com/api/reformat")
    AGENT_API_KEY = os.getenv("AGENT_API_KEY")
    
    if not AGENT_API_KEY:
        raise ValueError("AGENT_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    try:
        # Reformat Agent API 호출
        response = requests.post(
            AGENT_API_URL,
            headers={
                "Authorization": f"Bearer {AGENT_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "input": text,
                "output_format": "markdown_document",
                "include_metadata": True
            },
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # API 응답 파싱
        title = result.get("title", "Untitled Document")
        filename = result.get("filename", sanitize_filename(title))
        content = result.get("content", "")
        
        # 검증
        if not content:
            raise ValueError("Reformat Agent가 빈 내용을 반환했습니다.")
        
        return (title, filename, content)
        
    except requests.exceptions.RequestException as e:
        # API 호출 실패 시 에러 처리
        raise RuntimeError(f"Reformat Agent API 호출 실패: {str(e)}")
```

---

## 🔑 환경 변수 설정

### **필요한 환경 변수**

```bash
# .env 파일 또는 시스템 환경 변수
AGENT_REFORMAT_URL=https://agent-builder.company.com/api/reformat
AGENT_API_KEY=your-api-key-here
```

### **.env 파일 생성**

```bash
cd /path/to/agent-builder-automation
cat > .env << 'EOF'
# Agent Builder API Configuration
AGENT_REFORMAT_URL=https://agent-builder.company.com/api/reformat
AGENT_API_KEY=your-actual-api-key-here
EOF
```

### **Python에서 환경 변수 로드**

`doc_review_app.py` 상단에 추가:

```python
from dotenv import load_dotenv
import os

# .env 파일 로드 (파일 상단에 추가)
load_dotenv()
```

**설치 필요:**
```bash
pip install python-dotenv
```

---

## 📝 API 스펙 확인 사항

Cline과 함께 다음 정보를 확인하세요:

### **1. API 엔드포인트**
- [ ] URL: `https://...`
- [ ] 메서드: `POST` / `GET`
- [ ] 인증 방식: Bearer Token / API Key / OAuth

### **2. 요청 포맷**
```json
{
  "input": "사용자가 입력한 텍스트",
  "output_format": "markdown_document",
  "options": {
    "include_title": true,
    "include_filename": true,
    "language": "ko"
  }
}
```

### **3. 응답 포맷**
```json
{
  "title": "문서 제목",
  "filename": "document-filename",
  "content": "# Markdown 내용\n\n본문...",
  "metadata": {
    "category": "guides",
    "tags": ["ai", "documentation"]
  }
}
```

### **4. 에러 응답**
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "입력 텍스트가 너무 짧습니다."
  }
}
```

---

## 🧪 테스트 방법

### **Step 1: API 연결 테스트**

별도 Python 스크립트로 먼저 테스트:

```python
# test_reformat_api.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_reformat_api():
    url = os.getenv("AGENT_REFORMAT_URL")
    api_key = os.getenv("AGENT_API_KEY")
    
    test_text = """
    Python 최적화 팁
    
    1. 리스트 컴프리헨션
    빠른 속도
    
    2. 제너레이터
    메모리 절약
    """
    
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"input": test_text, "output_format": "markdown_document"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_reformat_api()
```

실행:
```bash
python test_reformat_api.py
```

### **Step 2: Streamlit 앱에서 테스트**

1. Streamlit 앱 실행:
```bash
cd agent-builder-automation
streamlit run doc_review_app.py
```

2. **Mode B (외부 AI 재구성)** 선택

3. 테스트 텍스트 입력:
```
Python 최적화 방법

리스트 컴프리헨션을 사용하면 빠릅니다.
제너레이터를 쓰면 메모리를 절약할 수 있습니다.
```

4. **"🔄 Reformat & Preview"** 클릭

5. 결과 확인:
   - ✅ 제목이 생성되었는가?
   - ✅ 파일명이 적절한가?
   - ✅ Markdown 구조가 올바른가?

---

## ⚠️ 주의사항

### **1. API 타임아웃**

Reformat Agent가 느릴 수 있으므로 타임아웃 설정:

```python
response = requests.post(
    AGENT_API_URL,
    ...,
    timeout=30  # 30초
)
```

### **2. 에러 처리**

```python
try:
    response = requests.post(...)
    response.raise_for_status()
except requests.exceptions.Timeout:
    raise RuntimeError("Reformat Agent 타임아웃 (30초 초과)")
except requests.exceptions.HTTPError as e:
    if response.status_code == 401:
        raise RuntimeError("API 인증 실패 - API 키를 확인하세요")
    elif response.status_code == 429:
        raise RuntimeError("API 호출 한도 초과 - 잠시 후 다시 시도하세요")
    else:
        raise RuntimeError(f"API 에러: {e}")
except Exception as e:
    raise RuntimeError(f"예상치 못한 오류: {e}")
```

### **3. 로컬 Fallback**

API가 실패하면 Mock 로직으로 대체:

```python
def reformat_external_text(text: str) -> tuple[str, str, str]:
    try:
        # 실제 API 호출
        return call_reformat_api(text)
    except Exception as e:
        st.warning(f"⚠️ Reformat Agent 호출 실패: {e}")
        st.info("💡 로컬 변환으로 대체합니다.")
        
        # Fallback to local mock
        return local_reformat(text)
```

---

## 🔄 API 응답 포맷 불일치 시

API 응답이 예상과 다를 경우 어댑터 함수 추가:

```python
def adapt_api_response(api_result: dict) -> tuple[str, str, str]:
    """
    API 응답을 내부 포맷으로 변환
    """
    # 케이스 1: title, filename, content가 직접 있는 경우
    if "title" in api_result and "content" in api_result:
        return (
            api_result["title"],
            api_result.get("filename", sanitize_filename(api_result["title"])),
            api_result["content"]
        )
    
    # 케이스 2: data 객체 안에 있는 경우
    if "data" in api_result:
        data = api_result["data"]
        return (
            data["title"],
            data.get("filename", sanitize_filename(data["title"])),
            data["content"]
        )
    
    # 케이스 3: 완전히 다른 포맷
    raise ValueError(f"알 수 없는 API 응답 포맷: {api_result}")
```

---

## 📊 체크리스트

작업 완료 시 아래 항목을 확인하세요:

### **설정**
- [ ] `.env` 파일 생성
- [ ] `AGENT_REFORMAT_URL` 설정
- [ ] `AGENT_API_KEY` 설정
- [ ] `python-dotenv` 설치

### **코드 수정**
- [ ] `reformat_external_text()` 함수 교체
- [ ] 환경 변수 로드 추가 (`load_dotenv()`)
- [ ] 에러 처리 추가
- [ ] (선택) Fallback 로직 추가

### **테스트**
- [ ] API 연결 테스트 (`test_reformat_api.py`)
- [ ] Streamlit Mode A 테스트 (기존 기능)
- [ ] Streamlit Mode B 테스트 (새 기능)
- [ ] 에러 케이스 테스트 (잘못된 API 키 등)

### **문서화**
- [ ] API 스펙 문서화
- [ ] 팀원 공유 (API 키 관리 방법 등)

---

## 🚀 배포 후 검증

### **1. 기능 검증**

```
[ ] Mode A (Agent Builder) 정상 작동
[ ] Mode B (외부 AI → Reformat) 정상 작동
[ ] Preview 정상 표시
[ ] Inbox 저장 정상
[ ] Publish 정상
[ ] GitHub Pages 배포 정상
```

### **2. 성능 검증**

```
[ ] API 응답 속도 (목표: 5초 이내)
[ ] 긴 텍스트 처리 (1000줄 이상)
[ ] 동시 요청 처리
```

### **3. 보안 검증**

```
[ ] API 키가 코드에 하드코딩되지 않음
[ ] .env 파일이 .gitignore에 포함됨
[ ] 로그에 API 키 노출 안 됨
```

---

## 📞 도움이 필요할 때

### **Cline에게 요청할 것**

1. **API 스펙 확인**
   - "사내 Reformat Agent API 문서를 찾아줘"
   - "API 인증 방법을 알려줘"

2. **코드 수정**
   - "`reformat_external_text` 함수를 사내 API로 교체해줘"
   - "에러 처리를 추가해줘"

3. **테스트**
   - "API 연결 테스트 스크립트를 만들어줘"
   - "Streamlit 앱에서 Mode B를 테스트해줘"

---

## 🎯 최종 목표

**외부 AI 복붙 결과 → 사내 Reformat Agent → 표준 Markdown → Inbox → Publish → GitHub Pages**

이 흐름이 완벽하게 작동하면 성공입니다! 🎉

---

**작성일:** 2026-03-07  
**작성자:** AI Documentation System Team  
**버전:** 1.0
