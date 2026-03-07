#!/usr/bin/env python3
"""
Export Agent 결과를 MkDocs docs 폴더에 저장하고 GitHub에 반영하는 스크립트

Usage:
    python export_agent_to_docs.py --input agent_output.txt --category analysis --build
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def parse_agent_output(text: str) -> tuple[str, str, str]:
    """
    Parse Export Agent output in the following format:

    TITLE:
    ...

    FILENAME:
    ...

    CONTENT:
    ...
    """
    pattern = re.compile(
        r"TITLE:\s*(?P<title>.*?)\s*FILENAME:\s*(?P<filename>.*?)\s*CONTENT:\s*(?P<content>.*)",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError("입력 텍스트에서 TITLE / FILENAME / CONTENT 블록을 찾지 못했습니다.")

    title = match.group("title").strip()
    filename = match.group("filename").strip()
    content = match.group("content").strip()

    if not title:
        raise ValueError("TITLE 값이 비어 있습니다.")
    if not filename:
        raise ValueError("FILENAME 값이 비어 있습니다.")
    if not content:
        raise ValueError("CONTENT 값이 비어 있습니다.")

    return title, filename, content


def sanitize_filename(filename: str) -> str:
    """
    Keep only lowercase letters, digits, and hyphens.
    """
    filename = filename.strip().lower()
    filename = filename.replace(" ", "-")
    filename = re.sub(r"[^a-z0-9\-]", "", filename)
    filename = re.sub(r"-{2,}", "-", filename).strip("-")

    if not filename:
        raise ValueError("유효한 파일명을 만들 수 없습니다.")

    return filename


def resolve_output_path(
    repo_root: Path,
    category: str,
    filename: str,
    overwrite: bool = False,
) -> Path:
    """
    Resolve output path for markdown file.
    Creates directory if not exists.
    Handles duplicate filenames with timestamp suffix.
    """
    docs_dir = repo_root / "docs" / category
    docs_dir.mkdir(parents=True, exist_ok=True)

    output_path = docs_dir / f"{filename}.md"

    if output_path.exists() and not overwrite:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = docs_dir / f"{filename}-{timestamp}.md"

    return output_path


def write_markdown_file(output_path: Path, content: str, dry_run: bool = False) -> None:
    """Write markdown content to file."""
    if dry_run:
        print(f"[DRY-RUN] 파일 저장 예정: {output_path}")
        return

    output_path.write_text(content, encoding="utf-8")
    print(f"[INFO] Markdown 저장 완료: {output_path}")


def run_command(
    command: list[str],
    cwd: Path,
    dry_run: bool = False,
) -> None:
    """Run shell command with error handling."""
    cmd_str = " ".join(command)
    if dry_run:
        print(f"[DRY-RUN] 실행 예정: {cmd_str}")
        return

    print(f"[INFO] 실행: {cmd_str}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"명령 실행 실패: {cmd_str}")

    if result.stdout.strip():
        print(result.stdout.strip())


def git_commit_and_push(
    repo_root: Path,
    filename: str,
    dry_run: bool = False,
) -> None:
    """Execute git add, commit, and push."""
    commit_message = f"add AI generated doc: {filename}"

    run_command(["git", "add", "."], cwd=repo_root, dry_run=dry_run)
    run_command(["git", "commit", "-m", commit_message], cwd=repo_root, dry_run=dry_run)
    run_command(["git", "push"], cwd=repo_root, dry_run=dry_run)


def run_mkdocs(
    repo_root: Path,
    build: bool = False,
    serve: bool = False,
    dry_run: bool = False,
) -> None:
    """Run mkdocs build or serve."""
    if build:
        run_command(["mkdocs", "build"], cwd=repo_root, dry_run=dry_run)

    if serve:
        print("[INFO] mkdocs serve를 실행합니다. Ctrl+C로 종료할 수 있습니다.")
        run_command(["mkdocs", "serve"], cwd=repo_root, dry_run=dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Agent 결과를 MkDocs docs 폴더에 저장하고 GitHub에 반영하는 스크립트"
    )
    parser.add_argument("--input", required=True, help="Export Agent 결과가 저장된 텍스트 파일 경로")
    parser.add_argument("--repo", default=".", help="MkDocs Git repository 루트 경로")
    parser.add_argument("--category", default="analysis", help="docs 하위 카테고리 폴더명")
    parser.add_argument("--overwrite", action="store_true", help="동일 파일이 있으면 덮어쓰기")
    parser.add_argument("--dry-run", action="store_true", help="실제 저장/실행 없이 동작만 출력")
    parser.add_argument("--build", action="store_true", help="저장 후 mkdocs build 실행")
    parser.add_argument("--serve", action="store_true", help="저장 후 mkdocs serve 실행")
    parser.add_argument("--skip-git", action="store_true", help="git add/commit/push 생략")

    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    repo_root = Path(args.repo).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {input_path}")

    # Parse input file
    raw_text = input_path.read_text(encoding="utf-8")
    title, filename, content = parse_agent_output(raw_text)
    safe_filename = sanitize_filename(filename)

    # Resolve output path
    output_path = resolve_output_path(
        repo_root=repo_root,
        category=args.category,
        filename=safe_filename,
        overwrite=args.overwrite,
    )

    # Display info
    print(f"[INFO] TITLE: {title}")
    print(f"[INFO] FILENAME: {safe_filename}")
    print(f"[INFO] OUTPUT PATH: {output_path}")

    # Write markdown file
    write_markdown_file(output_path, content, dry_run=args.dry_run)

    # Git operations
    if not args.skip_git:
        git_commit_and_push(repo_root, safe_filename, dry_run=args.dry_run)

    # MkDocs operations
    run_mkdocs(
        repo_root=repo_root,
        build=args.build,
        serve=args.serve,
        dry_run=args.dry_run,
    )

    print("[INFO] 작업 완료")


if __name__ == "__main__":
    main()
