# Documents Repository

개인 문서 및 자동화 도구 저장소

## 📁 프로젝트 구조

```
Documents/
├── agent-builder-automation/     # Agent Builder to MkDocs 자동화 도구
│   ├── export_agent_to_docs.py  # 메인 스크립트
│   ├── create_test_doc.py        # 테스트 생성기
│   ├── README.md                 # 상세 가이드
│   ├── QUICKSTART.md             # 빠른 시작 가이드
│   ├── TESTING_GUIDE.md          # 테스트 가이드
│   ├── SUMMARY.md                # 프로젝트 요약
│   ├── PROJECT_INFO.md           # 프로젝트 정보
│   └── docs/                     # 생성된 문서
│
├── images/                        # 이미지 자료
│
└── *.html                         # AI Agent 강의 자료
```

## 🚀 프로젝트

### 1. Agent Builder Automation

Agent Builder 결과를 자동으로 파싱하여 MkDocs 문서 저장소에 반영하는 자동화 도구

**시작하기**: [agent-builder-automation/QUICKSTART.md](agent-builder-automation/QUICKSTART.md)

**주요 기능**:
- ✅ Agent Builder Export 결과 파싱
- ✅ MkDocs 문서 자동 생성
- ✅ Git 자동화 (commit/push)
- ✅ 사외 환경 테스트 지원

**빠른 사용**:
```bash
cd agent-builder-automation
python create_test_doc.py "테스트 문서"
python export_agent_to_docs.py --input test_테스트-문서.txt --skip-git
```

## 📚 문서

### AI Agent 강의 자료
- `AI_Agent_강의안_Langflow_v3.html`
- `AI_Agent_강의안_Langflow_v10_최종.html`
- `AI_Agent_강의안_Langflow_v12_Vibe코딩_최종본_with_images.html`

## 🎯 저장소 목적

1. **개인 문서 관리**: 학습 자료 및 기술 문서
2. **자동화 도구**: 문서 생성 및 배포 자동화
3. **지식 공유**: 강의 자료 및 가이드

## 🔗 관련 링크

- [GitHub Repository](https://github.com/miniforce1119/Documents)

## 📅 업데이트

- **2026-03-07**: Agent Builder Automation 프로젝트 추가
- **2026-03-07**: 프로젝트 구조 정리

---

**Repository Owner**: miniforce1119
