# OpenClaw 원격 접속 가이드

## 📌 개요

**OpenClaw**는 집 PC의 개발 환경을 원격에서 안전하게 접속하여 사용할 수 있게 해주는 시스템입니다.  
Tailscale VPN과 HTTPS 프록시를 활용하여 외부에서도 안전하게 홈 서버에 접속할 수 있습니다.

---

## 🏗️ 시스템 아키텍처

```
[모바일/외부 PC]
       ↓ (Tailscale VPN)
[Tailscale HTTPS Proxy]
       ↓ (Port 18789)
[OpenClaw Docker Container]
       ↓
[집 PC 개발 환경]
```

### 주요 구성 요소

| 구성 요소 | 설명 |
|---------|------|
| **Tailscale** | Zero-config VPN으로 안전한 터널링 제공 |
| **OpenClaw Gateway** | Docker 컨테이너로 실행되는 원격 접속 게이트웨이 |
| **HTTPS Proxy** | Tailscale의 HTTPS 프록시 기능으로 보안 연결 |
| **WebSocket** | 실시간 양방향 통신 지원 |

---

## ⚙️ OpenClaw 설정

### 1. 설정 파일 위치
```
~/.openclaw/openclaw.json
```

### 2. 설정 파일 내용

```json
{
  "gateway": {
    "port": 18789,
    "token": "your-secret-token-here",
    "allowed_origins": [
      "https://your-device-name.tailxxxxx.ts.net",
      "http://localhost:*"
    ]
  }
}
```

> ⚠️ **보안 주의**: `token` 값은 본인만 알고 있는 안전한 문자열로 변경하세요.

#### 설정 항목 설명

| 항목 | 값 | 설명 |
|-----|---|------|
| `port` | 18789 | OpenClaw 게이트웨이가 실행되는 포트 |
| `token` | your-secret-token-here | 인증 토큰 (보안 키) - 반드시 변경 필요 |
| `allowed_origins` | 배열 | CORS 허용 도메인 목록 (본인의 Tailscale URL) |

---

## 🐳 Docker 컨테이너 관리

### 컨테이너 상태 확인

```bash
docker ps
```

**예상 출력:**
```
CONTAINER ID   IMAGE                  STATUS
abc123def456   openclaw-gateway:latest   Up (healthy)
```

### 컨테이너 이름
```
openclaw-openclaw-gateway-1
```

### Health Check 확인

```bash
docker inspect openclaw-openclaw-gateway-1 | grep Health -A 10
```

OpenClaw는 자체 health check를 실행하여 컨테이너 상태를 모니터링합니다.

---

## 🌐 Tailscale HTTPS 프록시 설정

### 1. Tailscale 서비스 시작

```bash
sudo tailscale serve -bg --https=443 http://127.0.0.1:18789
```

#### 옵션 설명
- `-bg`: 백그라운드로 실행
- `--https=443`: HTTPS 포트 443으로 프록시
- `http://127.0.0.1:18789`: OpenClaw 게이트웨이로 포워딩

### 2. Tailscale 상태 확인

```bash
tailscale status
```

**예상 출력:**
```
your-device-name  online
  100.x.x.x
  https://your-device-name.tailxxxxx.ts.net
```

> 💡 **참고**: `your-device-name`은 Tailscale에서 자동으로 생성되는 고유한 디바이스 이름입니다.

### 3. Tailscale Serve 설정 확인

```bash
tailscale serve status
```

**예상 출력:**
```
https://your-device-name.tailxxxxx.ts.net (tailnet only)
|-- / proxy http://127.0.0.1:18789
```

---

## 🔗 접속 URL

### HTTPS 접속
```
https://your-device-name.tailxxxxx.ts.net
```

### WebSocket 접속
```
wss://your-device-name.tailxxxxx.ts.net
```

> 📝 **내 Tailscale URL 확인 방법:**
> ```bash
> tailscale status
> ```
> 출력에서 `https://` 로 시작하는 URL을 확인하세요.

### 로컬 테스트 (집 PC에서)
```
http://localhost:18789
```

---

## 📱 모바일 접속 설정

### 1. Tailscale 앱 설치

- **iOS**: App Store에서 "Tailscale" 검색
- **Android**: Google Play에서 "Tailscale" 검색

### 2. Tailscale 로그인

1. Tailscale 앱 실행
2. 동일한 계정으로 로그인
3. VPN 연결 활성화

### 3. 디바이스 승인 (최초 1회)

집 PC에서 다음 명령 실행:
```bash
docker exec openclaw-openclaw-gateway-1 openclaw devices approve --latest
```

또는 모든 대기 중인 디바이스 승인:
```bash
docker exec openclaw-openclaw-gateway-1 openclaw devices approve --all
```

### 4. 접속 확인

모바일 브라우저에서:
```
https://your-device-name.tailxxxxx.ts.net
```

> 💡 본인의 Tailscale URL로 변경하세요.

---

## 🔧 문제 해결 (Troubleshooting)

### ❌ 문제 1: "접속할 수 없음" 오류

#### 해결 방법

**1단계: Tailscale Serve 상태 확인**
```bash
tailscale serve status
```

**예상 결과:**
```
https://your-device-name.tailxxxxx.ts.net (tailnet only)
|-- / proxy http://127.0.0.1:18789
```

만약 출력이 없다면:
```bash
sudo tailscale serve -bg --https=443 http://127.0.0.1:18789
```

**2단계: Docker 컨테이너 확인**
```bash
docker ps | grep openclaw
```

만약 컨테이너가 실행 중이 아니라면:
```bash
docker start openclaw-openclaw-gateway-1
```

**3단계: OpenClaw 게이트웨이 직접 확인**
```bash
curl http://localhost:18789
```

정상이라면 HTML 또는 JSON 응답을 받아야 합니다.

---

### ❌ 문제 2: DNS 이름으로 접속 불가

#### 증상
- `https://your-device-name.tailxxxxx.ts.net` 접속 불가
- "서버를 찾을 수 없음" 오류

#### 해결 방법

**1. Tailscale 연결 확인 (모바일)**
```
Tailscale 앱 > Status > "Connected" 확인
```

**2. DNS 설정 확인**

모바일에서:
1. **설정 > Wi-Fi > 고급 설정**
2. **DNS 설정 확인**
3. **Private DNS 비활성화** (일시적으로)

**3. 브라우저 캐시 삭제**

---

### ❌ 문제 3: HTTPS 인증서 오류

#### 증상
- "안전하지 않은 연결" 경고
- "인증서를 신뢰할 수 없음"

#### 원인
Tailscale HTTPS는 Tailscale이 발급한 자체 인증서를 사용합니다.

#### 해결 방법

**1. Tailscale 인증서 신뢰 설정**

iOS:
```
설정 > 일반 > VPN 및 기기 관리
> Tailscale 프로필 > 신뢰
```

Android:
```
설정 > 보안 > 인증서 관리
> Tailscale 인증서 신뢰
```

**2. 또는 브라우저에서 "계속 진행" 선택**

---

### ❌ 문제 4: WebSocket 연결 실패

#### 증상
- 초기 페이지는 로드되지만 실시간 기능 작동 안 함
- 콘솔 오류: `WebSocket connection failed`

#### 해결 방법

**1. allowed_origins 확인**

`~/.openclaw/openclaw.json` 파일에서:
```json
{
  "gateway": {
    "allowed_origins": [
      "https://your-device-name.tailxxxxx.ts.net"
    ]
  }
}
```

> 💡 본인의 Tailscale URL로 정확히 입력해야 합니다.

**2. OpenClaw 재시작**
```bash
docker restart openclaw-openclaw-gateway-1
```

**3. Tailscale Serve 재시작**
```bash
# 기존 서비스 중지
sudo tailscale serve reset

# 다시 시작
sudo tailscale serve -bg --https=443 http://127.0.0.1:18789
```

---

### ❌ 문제 5: 모바일에서 접속이 느림

#### 원인
Tailscale이 Relay 서버를 통해 우회 연결 중일 수 있음.

#### 해결 방법

**1. Tailscale Relay 상태 확인**
```bash
tailscale status
```

**출력 예시:**
```
your-device-name  online   relay "sfo"
mobile-device     online   relay "sfo"
```

`relay`가 표시되면 직접 연결이 아닌 우회 중입니다.

**2. 직접 연결 활성화**

집 PC 라우터에서:
- **UDP 포트 41641 포트 포워딩** 설정
- 또는 **UPnP 활성화**

**3. 방화벽 확인**

집 PC에서:
```bash
sudo ufw allow 41641/udp
```

---

## 🔐 보안 고려사항

### 1. 인증 토큰 관리

```bash
# 토큰 변경 (정기적으로 권장)
vi ~/.openclaw/openclaw.json
```

토큰 변경 후 OpenClaw 재시작 필수:
```bash
docker restart openclaw-openclaw-gateway-1
```

### 2. Tailscale 접근 제어

Tailscale Admin Console에서:
- **ACL(Access Control List) 설정**
- 특정 디바이스만 접근 허용

### 3. 로그 모니터링

```bash
docker logs openclaw-openclaw-gateway-1 --tail 100 -f
```

---

## ⚡ 서버 유지 관리

### 1. 집 PC 전원 관리

**Windows:**
```
제어판 > 전원 옵션 > 절전 모드 "사용 안 함"
```

**Linux:**
```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

### 2. WSL 자동 시작 (Windows)

`C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`에 배치:

**start-openclaw.bat:**
```batch
@echo off
wsl -d Ubuntu -u root -- bash -c "cd /path/to/openclaw && docker-compose up -d"
```

### 3. Docker 자동 재시작 설정

```bash
docker update --restart=always openclaw-openclaw-gateway-1
```

---

## 📊 상태 확인 명령어 모음

### 전체 상태 확인 스크립트

```bash
#!/bin/bash
echo "=== OpenClaw Status Check ==="
echo ""

echo "1. Docker Container Status:"
docker ps | grep openclaw
echo ""

echo "2. Tailscale Status:"
tailscale status
echo ""

echo "3. Tailscale Serve Status:"
tailscale serve status
echo ""

echo "4. OpenClaw Gateway Health:"
curl -s http://localhost:18789/health || echo "Gateway not responding"
echo ""

echo "5. Recent Logs:"
docker logs openclaw-openclaw-gateway-1 --tail 5
```

저장 후:
```bash
chmod +x check-openclaw.sh
./check-openclaw.sh
```

---

## 📚 추가 자료

### Tailscale 공식 문서
- [Tailscale Serve 가이드](https://tailscale.com/kb/1242/tailscale-serve/)
- [Tailscale HTTPS 설정](https://tailscale.com/kb/1153/enabling-https/)

### Docker 명령어 참고
```bash
# 컨테이너 로그 확인
docker logs openclaw-openclaw-gateway-1

# 컨테이너 내부 접속
docker exec -it openclaw-openclaw-gateway-1 bash

# 컨테이너 재시작
docker restart openclaw-openclaw-gateway-1

# 컨테이너 중지
docker stop openclaw-openclaw-gateway-1

# 컨테이너 시작
docker start openclaw-openclaw-gateway-1
```

---

## ❓ FAQ

### Q1: 외부 인터넷에서 접속이 안 되는데, 같은 Wi-Fi에서는 됩니다.

**A:** Tailscale VPN 연결이 필요합니다.  
모바일/외부 PC에 **Tailscale 앱을 설치하고 로그인**해야 합니다.

---

### Q2: 매번 디바이스 승인이 필요한가요?

**A:** 최초 1회만 승인하면 됩니다.  
이후에는 자동으로 연결됩니다.

승인 명령:
```bash
docker exec openclaw-openclaw-gateway-1 openclaw devices approve --latest
```

---

### Q3: 집 PC가 꺼져 있으면 접속이 안 되나요?

**A:** 네, 집 PC가 켜져 있어야 합니다.  
**Wake-on-LAN(WOL)** 기능을 활성화하면 원격에서 PC를 켤 수 있습니다.

---

### Q4: Tailscale 없이 접속할 수 있나요?

**A:** 가능하지만 보안상 권장하지 않습니다.  
공개 IP + 포트 포워딩 방식은 보안 위험이 있습니다.

---

### Q5: 여러 명이 동시에 접속할 수 있나요?

**A:** 네, OpenClaw는 다중 사용자 접속을 지원합니다.  
각 사용자는 Tailscale에 로그인한 후 동일한 URL로 접속하면 됩니다.

---

## 🎯 요약 체크리스트

### 초기 설정 (집 PC)
- [ ] OpenClaw Docker 컨테이너 실행
- [ ] `~/.openclaw/openclaw.json` 설정 확인
- [ ] Tailscale 설치 및 로그인
- [ ] `tailscale serve -bg --https=443 http://127.0.0.1:18789` 실행
- [ ] `tailscale serve status`로 확인

### 모바일 설정
- [ ] Tailscale 앱 설치
- [ ] Tailscale 로그인 (동일 계정)
- [ ] VPN 연결 활성화
- [ ] 집 PC에서 디바이스 승인
- [ ] `https://your-device-name.tailxxxxx.ts.net` 접속 테스트 (본인 URL)

### 문제 발생 시
- [ ] `docker ps` - 컨테이너 실행 확인
- [ ] `tailscale status` - VPN 연결 확인
- [ ] `tailscale serve status` - 프록시 상태 확인
- [ ] `curl http://localhost:18789` - 게이트웨이 응답 확인
- [ ] 브라우저 캐시 삭제
- [ ] Private DNS 비활성화 (일시적)

---

## 📞 지원

추가 문제가 발생하면:
1. `docker logs openclaw-openclaw-gateway-1` 로그 확인
2. Tailscale 커뮤니티 포럼 검색
3. OpenClaw GitHub Issues 등록

---

**문서 버전:** 1.0  
**최종 수정일:** 2026-03-15  
**작성자:** AI Documentation System
