# Docker 배포 완벽 가이드

> 생성일: 2026-03-07  
> 카테고리: guides  
> 작성자: AI Agent

## 📋 개요

이 문서는 Docker를 활용한 애플리케이션 배포의 모든 과정을 다룹니다.

## 🎯 목표

- Docker 기본 개념 이해
- 실전 배포 전략 수립
- CI/CD 파이프라인 구축

## 🐳 Docker 기본

### Docker란?

Docker는 컨테이너 기반의 가상화 플랫폼입니다.

**주요 특징:**
- 경량화된 가상화
- 이식성 (Portability)
- 빠른 배포 속도
- 일관된 환경 제공

### 핵심 개념

| 개념 | 설명 | 용도 |
|------|------|------|
| **이미지** | 실행 가능한 패키지 | 애플리케이션 템플릿 |
| **컨테이너** | 이미지의 실행 인스턴스 | 실제 실행 환경 |
| **레지스트리** | 이미지 저장소 | Docker Hub, ECR 등 |
| **볼륨** | 데이터 영속성 | 데이터 저장 |

## 📦 Dockerfile 작성

### Python 애플리케이션 예제

```dockerfile
# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Node.js 애플리케이션 예제

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application
COPY . .

# Build
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

## 🚀 빌드 및 실행

### 기본 명령어

```bash
# 이미지 빌드
docker build -t myapp:1.0.0 .

# 컨테이너 실행
docker run -d \
  --name myapp \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  myapp:1.0.0

# 컨테이너 로그 확인
docker logs -f myapp

# 컨테이너 상태 확인
docker ps

# 컨테이너 중지
docker stop myapp

# 컨테이너 삭제
docker rm myapp
```

### Docker Compose 활용

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
```

## 🔧 최적화 기법

### 1. 멀티 스테이지 빌드

```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### 2. 레이어 캐싱 활용

```dockerfile
# ❌ 비효율적
COPY . .
RUN pip install -r requirements.txt

# ✅ 효율적 - 의존성 캐싱
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 3. .dockerignore 사용

```
node_modules
npm-debug.log
.git
.env
*.md
.DS_Store
__pycache__
*.pyc
.pytest_cache
coverage/
```

## 🔐 보안 Best Practices

### 1. Non-root 사용자

```dockerfile
FROM python:3.12-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

CMD ["python", "app.py"]
```

### 2. 최소 권한 원칙

```dockerfile
# ✅ 필요한 파일만 복사
COPY requirements.txt .
COPY src/ ./src/
COPY config/ ./config/

# ❌ 전체 복사 지양
# COPY . .
```

### 3. 비밀 정보 관리

```bash
# Docker secrets 사용
docker secret create db_password password.txt

docker service create \
  --name myapp \
  --secret db_password \
  myapp:latest
```

## 📊 모니터링

### 헬스체크 구현

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

### 로깅 설정

```bash
# JSON 형식 로깅
docker run -d \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myapp:latest
```

## 🔄 CI/CD 통합

### GitHub Actions 예제

```yaml
name: Docker Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            myapp:latest
            myapp:${{ github.sha }}
```

## 🎓 실전 배포 체크리스트

### 배포 전

- [ ] Dockerfile 최적화 완료
- [ ] 멀티 스테이지 빌드 적용
- [ ] .dockerignore 설정
- [ ] 헬스체크 구현
- [ ] 환경 변수 설정
- [ ] 볼륨 마운트 계획
- [ ] 네트워크 구성 검토

### 배포 중

- [ ] 이미지 빌드 성공
- [ ] 이미지 레지스트리 푸시
- [ ] 컨테이너 실행 확인
- [ ] 헬스체크 통과
- [ ] 로그 모니터링
- [ ] 성능 메트릭 확인

### 배포 후

- [ ] 애플리케이션 동작 확인
- [ ] 데이터 마이그레이션 검증
- [ ] 백업 설정 완료
- [ ] 모니터링 대시보드 구성
- [ ] 장애 복구 절차 준비

## 📚 참고 자료

- [Docker 공식 문서](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🔍 트러블슈팅

### 이미지 크기가 큰 경우

```bash
# 이미지 레이어 분석
docker history myapp:latest

# 불필요한 레이어 제거
docker image prune
```

### 컨테이너가 시작 직후 종료되는 경우

```bash
# 로그 확인
docker logs myapp

# 인터랙티브 모드로 실행
docker run -it myapp:latest /bin/sh
```

### 네트워크 연결 문제

```bash
# 네트워크 확인
docker network ls

# 컨테이너 네트워크 상세 정보
docker network inspect bridge
```

## 💡 주요 포인트

1. **경량화**: Alpine 이미지 사용, 멀티 스테이지 빌드
2. **보안**: Non-root 사용자, 최소 권한
3. **효율성**: 레이어 캐싱, .dockerignore
4. **신뢰성**: 헬스체크, 로깅, 모니터링
5. **자동화**: CI/CD 파이프라인 구축

---

**작성일:** 2026-03-07  
**카테고리:** Guides  
**태그:** #docker #deployment #devops #containers #cicd