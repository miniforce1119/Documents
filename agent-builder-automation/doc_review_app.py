#!/usr/bin/env python3
"""
AI Document Review & Publish System

Two-Mode Documentation System:
- Mode A: Agent Builder Direct Import (formatted)
- Mode B: External AI Reformat (free-form text)

Both modes converge to normalized format:
  TITLE: ...
  FILENAME: ...
  CONTENT: # Markdown...
"""

import streamlit as st
import re
import subprocess
from pathlib import Path
from datetime import datetime
import json

# 페이지 설정
st.set_page_config(
    page_title="Document Review & Publish",
    page_icon="📝",
    layout="wide"
)

# 경로 설정
BASE_DIR = Path(__file__).parent
INBOX_DIR = BASE_DIR / "inbox"
PUBLISHED_DIR = BASE_DIR / "published"
DOCS_DIR = BASE_DIR / "docs"

INBOX_DIR.mkdir(exist_ok=True)
PUBLISHED_DIR.mkdir(exist_ok=True)


def parse_agent_output(text: str) -> tuple[str, str, str]:
    """Agent Builder 출력 파싱 (Mode A)"""
    pattern = re.compile(
        r"TITLE:\s*(?P<title>.*?)\s*FILENAME:\s*(?P<filename>.*?)\s*CONTENT:\s*(?P<content>.*)",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError("TITLE/FILENAME/CONTENT 블록을 찾을 수 없습니다.")
    
    return (
        match.group("title").strip(),
        match.group("filename").strip(),
        match.group("content").strip()
    )


def detect_input_mode(text: str) -> str:
    """입력 모드 자동 감지"""
    if "TITLE:" in text and "FILENAME:" in text and "CONTENT:" in text:
        return "agent_builder"
    return "external_ai"


def reformat_external_text(text: str) -> tuple[str, str, str]:
    """
    외부 AI 텍스트를 표준 Markdown 문서로 재구성 (Mode B)
    
    TODO (for Cline at company):
    이 함수를 사내 Reformat Agent API로 교체:
    
    def reformat_external_text(text: str) -> tuple[str, str, str]:
        import requests
        response = requests.post(
            "https://company-agent-builder.com/api/reformat",
            headers={"Authorization": f"Bearer {AGENT_API_KEY}"},
            json={"input": text, "output_format": "markdown_document"}
        )
        result = response.json()
        return (result["title"], result["filename"], result["content"])
    """
    # Mock implementation for testing
    lines = text.strip().split('\n')
    
    # 제목 추출 (첫 줄 또는 # 헤더)
    title = lines[0].strip('#').strip() if lines else "Untitled Document"
    
    # 파일명 생성
    filename = sanitize_filename(title)
    
    # Markdown 변환
    content = f"# {title}\n\n"
    content += f"> 생성일: {datetime.now().strftime('%Y-%m-%d')}\n"
    content += f"> 출처: 외부 AI\n\n"
    
    # 본문 처리
    in_code_block = False
    for i, line in enumerate(lines[1:] if len(lines) > 1 else lines):
        line = line.rstrip()
        
        # 코드 블록 감지
        if line.startswith('```') or line.startswith('    '):
            in_code_block = not in_code_block
        
        # 구조화
        if not in_code_block:
            # 숫자로 시작하는 줄 → 서브헤더
            if re.match(r'^\d+\.\s+', line):
                content += f"\n## {line}\n"
            # 짧은 줄 뒤에 긴 설명 → 리스트
            elif line and not line.startswith('#'):
                if len(line) < 50 and i + 1 < len(lines) and lines[i + 1]:
                    content += f"\n### {line}\n\n"
                else:
                    content += f"{line}\n"
            else:
                content += f"{line}\n"
        else:
            content += f"{line}\n"
    
    return (title, filename, content)


def sanitize_filename(filename: str) -> str:
    """파일명 정리"""
    filename = filename.strip().lower()
    filename = filename.replace(" ", "-")
    filename = re.sub(r"[^a-z0-9\-가-힣]", "", filename)
    filename = re.sub(r"-{2,}", "-", filename).strip("-")
    return filename or "untitled"


def save_to_inbox(title: str, filename: str, content: str, metadata: dict) -> Path:
    """Inbox에 저장"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_filename = sanitize_filename(filename)
    inbox_file = INBOX_DIR / f"{timestamp}_{safe_filename}.md"
    
    # 메타데이터를 YAML frontmatter로 추가
    full_content = f"""---
title: {title}
filename: {safe_filename}
category: {metadata.get('category', 'analysis')}
tags: {', '.join(metadata.get('tags', []))}
created: {timestamp}
status: inbox
---

{content}
"""
    
    inbox_file.write_text(full_content, encoding="utf-8")
    return inbox_file


def load_inbox_files():
    """Inbox 파일 목록 로드"""
    files = sorted(INBOX_DIR.glob("*.md"), reverse=True)
    return files


def load_file_content(file_path: Path) -> tuple[dict, str]:
    """파일 내용과 메타데이터 로드"""
    content = file_path.read_text(encoding="utf-8")
    
    # YAML frontmatter 파싱
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            metadata_text = parts[1]
            body = parts[2].strip()
            
            metadata = {}
            for line in metadata_text.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
            
            return metadata, body
    
    return {}, content


def publish_document(inbox_file: Path, category: str, title: str, filename: str):
    """문서 발행"""
    # 메타데이터와 내용 로드
    metadata, content = load_file_content(inbox_file)
    
    # Published 폴더에 저장
    safe_filename = sanitize_filename(filename)
    published_file = PUBLISHED_DIR / f"{safe_filename}.md"
    published_file.write_text(content, encoding="utf-8")
    
    # docs 폴더에 저장
    category_dir = DOCS_DIR / category
    category_dir.mkdir(exist_ok=True, parents=True)
    docs_file = category_dir / f"{safe_filename}.md"
    docs_file.write_text(content, encoding="utf-8")
    
    # Inbox에서 삭제
    inbox_file.unlink()
    
    return docs_file


def git_commit_and_push(message: str):
    """Git commit 및 push, 그리고 GitHub Pages 자동 배포"""
    try:
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
        
        # GitHub Pages 자동 배포
        subprocess.run(["mkdocs", "gh-deploy", "--force"], cwd=BASE_DIR, check=True)
        
        return True, "Git push 및 GitHub Pages 배포 완료!"
    except subprocess.CalledProcessError as e:
        return False, f"오류: {str(e)}"


def get_mkdocs_url(category: str, filename: str) -> str:
    """MkDocs 문서 URL 생성"""
    # 로컬 개발 서버 URL (기본 포트 8000)
    base_url = "https://8000-i395tla92yet3fwt6gb1m-5185f4aa.sandbox.novita.ai/Documents"
    return f"{base_url}/{category}/{filename}/"


# Streamlit UI
st.title("📝 AI Document Review & Publish")
st.markdown("AI 생성 문서 검토 및 발행 시스템 (2-Mode)")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📥 Save to Inbox", "📋 Review Inbox", "📊 Published Docs"])

# Tab 1: Save to Inbox
with tab1:
    st.header("📥 AI 결과를 Inbox에 저장")
    
    # 입력 모드 선택
    input_mode = st.radio(
        "입력 모드 선택",
        ["Agent Builder (정형)", "외부 AI (재구성)"],
        horizontal=True,
        help="Agent Builder: 정형화된 TITLE/FILENAME/CONTENT 포맷\n외부 AI: ChatGPT/Claude 등 자유 텍스트"
    )
    
    if input_mode == "Agent Builder (정형)":
        st.markdown("""
        ### 📋 Mode A: Agent Builder Direct Import
        1. 사내 Agent Builder 결과 복사
        2. 아래에 붙여넣기 (TITLE/FILENAME/CONTENT 포맷)
        3. Parse & Preview
        4. Save to Inbox
        """)
        
        agent_output = st.text_area(
            "Agent Builder 결과 붙여넣기",
            height=200,
            placeholder="""TITLE:
문서 제목

FILENAME:
파일명

CONTENT:
# Markdown 내용
...""",
            key="agent_input"
        )
        
        button_label = "🔍 Parse & Preview"
        
    else:  # 외부 AI
        st.markdown("""
        ### 🔄 Mode B: External AI Reformat
        1. ChatGPT/Claude 등 외부 AI 답변 복사
        2. 아래에 붙여넣기 (자유 형식)
        3. Reformat & Preview (자동으로 표준 포맷으로 변환)
        4. Save to Inbox
        
        **Note:** 회사에서는 사내 Reformat Agent가 더 정교하게 변환합니다.
        """)
        
        agent_output = st.text_area(
            "외부 AI 결과 붙여넣기",
            height=200,
            placeholder="""예시:

Python 최적화 팁

1. 리스트 컴프리헨션 사용
빠르고 간결한 코드 작성 가능

2. 제너레이터 활용
메모리 효율적인 처리

...""",
            key="external_input"
        )
        
        button_label = "🔄 Reformat & Preview"
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(button_label, type="primary"):
            if agent_output:
                try:
                    if input_mode == "Agent Builder (정형)":
                        title, filename, content = parse_agent_output(agent_output)
                    else:
                        title, filename, content = reformat_external_text(agent_output)
                    
                    st.session_state['parsed'] = {
                        'title': title,
                        'filename': filename,
                        'content': content,
                        'mode': input_mode
                    }
                    st.success(f"✅ 처리 성공! (Mode: {input_mode})")
                except Exception as e:
                    st.error(f"❌ 처리 실패: {str(e)}")
            else:
                st.warning("⚠️ 텍스트를 입력해주세요.")
    
    # Preview 영역
    if 'parsed' in st.session_state:
        st.markdown("---")
        st.subheader("📄 Preview")
        
        parsed = st.session_state['parsed']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**메타데이터**")
            st.write(f"**제목:** {parsed['title']}")
            st.write(f"**파일명:** {parsed['filename']}")
            st.write(f"**입력 모드:** {parsed.get('mode', 'N/A')}")
            
            category = st.selectbox(
                "카테고리",
                ["analysis", "guides", "reports", "concepts"],
                key="save_category"
            )
            
            tags_input = st.text_input("태그 (쉼표로 구분)", "")
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        
        with col2:
            st.markdown("**Markdown Preview**")
            st.markdown(parsed['content'])
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("💾 Save to Inbox", type="primary"):
                try:
                    metadata = {
                        'category': category,
                        'tags': tags
                    }
                    inbox_file = save_to_inbox(
                        parsed['title'],
                        parsed['filename'],
                        parsed['content'],
                        metadata
                    )
                    st.success(f"✅ Inbox에 저장됨: {inbox_file.name}")
                    del st.session_state['parsed']
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 저장 실패: {str(e)}")
        
        with col2:
            if st.button("🗑️ Clear"):
                del st.session_state['parsed']
                st.rerun()

# Tab 2: Review Inbox
with tab2:
    st.header("📋 Inbox 문서 검토")
    
    inbox_files = load_inbox_files()
    
    if not inbox_files:
        st.info("📭 Inbox가 비어있습니다.")
    else:
        st.write(f"**총 {len(inbox_files)}개의 문서**")
        
        # 파일 선택
        selected_file = st.selectbox(
            "문서 선택",
            inbox_files,
            format_func=lambda x: x.name
        )
        
        if selected_file:
            metadata, content = load_file_content(selected_file)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**메타데이터**")
                st.write(f"**제목:** {metadata.get('title', 'N/A')}")
                st.write(f"**파일명:** {metadata.get('filename', 'N/A')}")
                st.write(f"**카테고리:** {metadata.get('category', 'analysis')}")
                st.write(f"**생성일:** {metadata.get('created', 'N/A')}")
                
                st.markdown("---")
                
                # 발행 옵션
                st.markdown("**발행 설정**")
                publish_title = st.text_input("제목", metadata.get('title', ''))
                publish_filename = st.text_input("파일명", metadata.get('filename', ''))
                publish_category = st.selectbox(
                    "카테고리",
                    ["analysis", "guides", "reports", "concepts"],
                    index=["analysis", "guides", "reports", "concepts"].index(
                        metadata.get('category', 'analysis')
                    )
                )
            
            with col2:
                st.markdown("**Preview**")
                st.markdown(content)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🚀 Publish", type="primary"):
                    try:
                        docs_file = publish_document(
                            selected_file,
                            publish_category,
                            publish_title,
                            publish_filename
                        )
                        st.success(f"✅ 발행 완료: {docs_file}")
                        
                        # MkDocs URL 생성
                        mkdocs_url = get_mkdocs_url(publish_category, publish_filename)
                        
                        # Git push
                        if st.checkbox("Git push", value=True):
                            success, message = git_commit_and_push(
                                f"docs: publish {publish_filename}"
                            )
                            if success:
                                st.success(message)
                            else:
                                st.warning(message)
                        
                        # MkDocs 문서 링크 표시
                        st.markdown("---")
                        st.markdown("### 📖 발행된 문서 확인")
                        st.link_button(
                            "🌐 MkDocs에서 보기",
                            mkdocs_url,
                            use_container_width=True
                        )
                        st.info(f"💡 MkDocs 서버가 실행 중이어야 합니다. (포트 8000)")
                        
                        # 자동 새로고침 대신 수동으로 제어
                        if st.button("✅ 완료"):
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ 발행 실패: {str(e)}")
            
            with col2:
                if st.button("🗑️ Delete"):
                    selected_file.unlink()
                    st.success("✅ 삭제 완료")
                    st.rerun()

# Tab 3: Published Docs
with tab3:
    st.header("📊 발행된 문서")
    
    published_files = sorted(PUBLISHED_DIR.glob("*.md"), reverse=True)
    
    if not published_files:
        st.info("📭 발행된 문서가 없습니다.")
    else:
        st.write(f"**총 {len(published_files)}개의 발행 문서**")
        
        for file in published_files:
            with st.expander(file.name):
                content = file.read_text(encoding="utf-8")
                st.markdown(content[:500] + "..." if len(content) > 500 else content)
                
                if st.button(f"🔗 Open in docs", key=f"open_{file.name}"):
                    st.info(f"docs/ 폴더에서 확인하세요: {file.name}")

# Sidebar
with st.sidebar:
    st.header("⚙️ 설정")
    
    st.markdown("### 📂 경로")
    st.code(f"Inbox: {INBOX_DIR}")
    st.code(f"Published: {PUBLISHED_DIR}")
    st.code(f"Docs: {DOCS_DIR}")
    
    st.markdown("---")
    
    st.markdown("### 📊 통계")
    inbox_count = len(list(INBOX_DIR.glob("*.md")))
    published_count = len(list(PUBLISHED_DIR.glob("*.md")))
    
    st.metric("Inbox", inbox_count)
    st.metric("Published", published_count)
    
    st.markdown("---")
    
    st.markdown("### 🔗 링크")
    st.markdown("[📖 GitHub](https://github.com/miniforce1119/Documents)")
    st.markdown("[🌐 Docs Site](https://miniforce1119.github.io/Documents/)")
    
    st.markdown("---")
    
    if st.button("🔄 Refresh"):
        st.rerun()
