#!/usr/bin/env python3
"""
Agent Builder Document Review & Publish App
Streamlit 기반 문서 검토 및 발행 도구
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
    """Agent Builder 출력 파싱"""
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
    """Git commit 및 push"""
    try:
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
        return True, "Git push 성공!"
    except subprocess.CalledProcessError as e:
        return False, f"Git 오류: {str(e)}"


# Streamlit UI
st.title("📝 Document Review & Publish")
st.markdown("Agent Builder 문서 검토 및 발행 시스템")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📥 Save to Inbox", "📋 Review Inbox", "📊 Published Docs"])

# Tab 1: Save to Inbox
with tab1:
    st.header("📥 Agent 결과를 Inbox에 저장")
    
    st.markdown("""
    ### 사용 방법
    1. Agent Builder 결과를 복사
    2. 아래에 붙여넣기
    3. Preview 확인
    4. Save to Inbox 클릭
    """)
    
    # 입력 영역
    agent_output = st.text_area(
        "Agent Builder 결과 붙여넣기",
        height=200,
        placeholder="""TITLE:
문서 제목

FILENAME:
파일명

CONTENT:
# Markdown 내용
..."""
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Parse & Preview", type="primary"):
            if agent_output:
                try:
                    title, filename, content = parse_agent_output(agent_output)
                    st.session_state['parsed'] = {
                        'title': title,
                        'filename': filename,
                        'content': content
                    }
                    st.success("✅ 파싱 성공!")
                except ValueError as e:
                    st.error(f"❌ 파싱 실패: {str(e)}")
            else:
                st.warning("⚠️ Agent 결과를 입력해주세요.")
    
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
                        
                        # Git push
                        if st.checkbox("Git push", value=True):
                            success, message = git_commit_and_push(
                                f"docs: publish {publish_filename}"
                            )
                            if success:
                                st.success(message)
                            else:
                                st.warning(message)
                        
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
