# RESTful API 설계 완벽 가이드

> 생성일: 2026-03-07  
> 카테고리: guides  
> 작성자: API Design Team

## 📋 개요

현대적인 RESTful API 설계 원칙과 모범 사례를 다루는 실전 가이드입니다.

## 🎯 목표

- REST 아키텍처 원칙 이해
- API 설계 Best Practices 습득
- 실전에서 바로 적용 가능한 패턴 학습
- 보안과 성능을 고려한 설계

## 🏗️ REST 기본 원칙

### REST란?

**RE**presentational **S**tate **T**ransfer - 자원을 표현하고 상태를 전달하는 아키텍처 스타일

### 핵심 제약 조건

| 원칙 | 설명 | 예시 |
|------|------|------|
| **Client-Server** | 클라이언트와 서버 분리 | 프론트엔드 ↔ 백엔드 |
| **Stateless** | 무상태성 | 각 요청은 독립적 |
| **Cacheable** | 캐시 가능 | GET 요청 캐싱 |
| **Uniform Interface** | 일관된 인터페이스 | 표준 HTTP 메서드 |
| **Layered System** | 계층화 시스템 | 로드밸런서, 프록시 |

## 🔤 리소스 명명 규칙

### URL 설계 원칙

```
✅ 좋은 예:
GET    /api/v1/users              # 사용자 목록
GET    /api/v1/users/123          # 특정 사용자
POST   /api/v1/users              # 사용자 생성
PUT    /api/v1/users/123          # 사용자 전체 수정
PATCH  /api/v1/users/123          # 사용자 부분 수정
DELETE /api/v1/users/123          # 사용자 삭제

GET    /api/v1/users/123/posts    # 특정 사용자의 게시글
GET    /api/v1/posts?author=123   # 쿼리 파라미터 활용

❌ 나쁜 예:
GET    /api/v1/getUser?id=123     # 동사 사용 지양
POST   /api/v1/user/create        # 동사 중복
GET    /api/v1/Users              # 대문자 사용
DELETE /api/v1/delete-user/123    # 하이픈과 동사
```

### 명명 규칙

```bash
# ✅ 복수형 명사 사용
/users
/products
/orders

# ✅ 케밥 케이스 (kebab-case)
/user-profiles
/order-items
/shipping-addresses

# ✅ 명확한 계층 구조
/organizations/123/teams/456/members

# ✅ 필터링은 쿼리 파라미터
/products?category=electronics&price_min=100&price_max=500
/users?role=admin&status=active&page=2&limit=20
```

## 🔀 HTTP 메서드

### 표준 메서드 활용

```http
# ✅ GET - 조회 (안전, 멱등)
GET /api/v1/users/123
Response: 200 OK
{
  "id": 123,
  "name": "홍길동",
  "email": "hong@example.com"
}

# ✅ POST - 생성 (비멱등)
POST /api/v1/users
Content-Type: application/json
{
  "name": "김철수",
  "email": "kim@example.com"
}
Response: 201 Created
Location: /api/v1/users/124

# ✅ PUT - 전체 수정 (멱등)
PUT /api/v1/users/123
Content-Type: application/json
{
  "name": "홍길동",
  "email": "hong.new@example.com",
  "phone": "010-1234-5678"
}
Response: 200 OK

# ✅ PATCH - 부분 수정 (멱등)
PATCH /api/v1/users/123
Content-Type: application/json
{
  "email": "hong.updated@example.com"
}
Response: 200 OK

# ✅ DELETE - 삭제 (멱등)
DELETE /api/v1/users/123
Response: 204 No Content
```

### 멱등성 (Idempotency)

| 메서드 | 안전 | 멱등 | 설명 |
|--------|------|------|------|
| GET | ✅ | ✅ | 여러 번 호출해도 같은 결과 |
| POST | ❌ | ❌ | 호출마다 새 리소스 생성 |
| PUT | ❌ | ✅ | 여러 번 호출해도 같은 상태 |
| PATCH | ❌ | ✅ | 구현에 따라 다를 수 있음 |
| DELETE | ❌ | ✅ | 여러 번 삭제해도 같은 결과 |

## 📊 응답 설계

### HTTP 상태 코드

```http
# ✅ 2xx - 성공
200 OK              # 성공 (일반)
201 Created         # 리소스 생성 성공
204 No Content      # 성공했지만 응답 본문 없음
206 Partial Content # 부분 컨텐츠

# ✅ 3xx - 리다이렉션
301 Moved Permanently  # 영구 이동
302 Found             # 임시 이동
304 Not Modified      # 캐시 사용 가능

# ✅ 4xx - 클라이언트 오류
400 Bad Request       # 잘못된 요청
401 Unauthorized      # 인증 필요
403 Forbidden         # 권한 없음
404 Not Found         # 리소스 없음
409 Conflict          # 충돌 (중복 리소스 등)
422 Unprocessable Entity  # 유효성 검증 실패
429 Too Many Requests     # 속도 제한

# ✅ 5xx - 서버 오류
500 Internal Server Error  # 서버 내부 오류
502 Bad Gateway           # 게이트웨이 오류
503 Service Unavailable   # 서비스 이용 불가
504 Gateway Timeout       # 게이트웨이 타임아웃
```

### 응답 포맷

```json
// ✅ 성공 응답
{
  "data": {
    "id": 123,
    "name": "홍길동",
    "email": "hong@example.com",
    "created_at": "2026-03-07T10:30:00Z"
  },
  "meta": {
    "timestamp": "2026-03-07T10:30:05Z",
    "version": "1.0"
  }
}

// ✅ 목록 응답 (페이징)
{
  "data": [
    {"id": 1, "name": "User 1"},
    {"id": 2, "name": "User 2"}
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  },
  "links": {
    "self": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=2",
    "prev": null,
    "first": "/api/v1/users?page=1",
    "last": "/api/v1/users?page=5"
  }
}

// ✅ 에러 응답
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력값이 유효하지 않습니다.",
    "details": [
      {
        "field": "email",
        "message": "이메일 형식이 올바르지 않습니다."
      },
      {
        "field": "password",
        "message": "비밀번호는 최소 8자 이상이어야 합니다."
      }
    ]
  },
  "meta": {
    "timestamp": "2026-03-07T10:30:05Z",
    "request_id": "abc123"
  }
}
```

## 🔍 필터링, 정렬, 검색

### 쿼리 파라미터 활용

```http
# ✅ 필터링
GET /api/v1/products?category=electronics&price_min=100&price_max=500
GET /api/v1/users?status=active&role=admin

# ✅ 정렬
GET /api/v1/products?sort=price_asc
GET /api/v1/products?sort=-created_at  # 내림차순 (-)
GET /api/v1/products?sort=category,price_desc  # 다중 정렬

# ✅ 페이징
GET /api/v1/users?page=2&limit=20
GET /api/v1/users?offset=40&limit=20

# ✅ 필드 선택 (Sparse Fieldsets)
GET /api/v1/users?fields=id,name,email
GET /api/v1/products?fields=id,name,price&include=category

# ✅ 검색
GET /api/v1/products?q=laptop
GET /api/v1/users?search=홍길동

# ✅ 복합 쿼리
GET /api/v1/products?category=laptop&price_max=2000&sort=price_asc&page=1&limit=20
```

## 🔐 인증 및 보안

### API 키 방식

```http
# ✅ 헤더 방식 (권장)
GET /api/v1/users
X-API-Key: your-api-key-here

# ✅ Bearer Token (JWT)
GET /api/v1/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# ❌ 쿼리 파라미터 (보안 취약)
GET /api/v1/users?api_key=your-key  # 로그에 노출 위험!
```

### OAuth 2.0 예제

```http
# 1. 액세스 토큰 발급
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=your_client_id&
client_secret=your_client_secret

Response:
{
  "access_token": "abc123...",
  "token_type": "Bearer",
  "expires_in": 3600
}

# 2. API 호출
GET /api/v1/users
Authorization: Bearer abc123...
```

### CORS 설정

```http
# Preflight 요청
OPTIONS /api/v1/users
Origin: https://example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type

# 응답
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

## ⚡ 성능 최적화

### 캐싱

```http
# ✅ ETag 사용
GET /api/v1/users/123
Response:
HTTP/1.1 200 OK
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Cache-Control: max-age=3600

# 조건부 요청
GET /api/v1/users/123
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Response:
HTTP/1.1 304 Not Modified
```

### Rate Limiting

```http
# ✅ 속도 제한 헤더
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1678886400

# 제한 초과 시
HTTP/1.1 429 Too Many Requests
Retry-After: 3600
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API 호출 한도를 초과했습니다. 1시간 후 다시 시도하세요."
  }
}
```

### 압축

```http
# ✅ Gzip 압축
GET /api/v1/users
Accept-Encoding: gzip, deflate

Response:
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Length: 1234
```

## 📚 버전 관리

### 버전 관리 전략

```http
# ✅ URL 버전 (권장)
GET /api/v1/users
GET /api/v2/users

# ✅ 헤더 버전
GET /api/users
Accept: application/vnd.myapi.v2+json

# ✅ 쿼리 파라미터
GET /api/users?version=2

# 버전 관리 정책
- v1: 안정 버전 (2024-01-01 ~ 2026-12-31)
- v2: 현재 버전 (2025-01-01 ~ )
- v3: 베타 버전 (2026-01-01 ~ )
```

## 🧪 API 문서화

### OpenAPI (Swagger) 예제

```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
  description: 사용자 관리 RESTful API

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /users:
    get:
      summary: 사용자 목록 조회
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 성공
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
    post:
      summary: 사용자 생성
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: 생성됨
        '400':
          description: 잘못된 요청

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
```

## ✅ 체크리스트

### API 설계 전

- [ ] 리소스 모델링 완료
- [ ] URL 구조 설계
- [ ] HTTP 메서드 선택
- [ ] 응답 포맷 정의
- [ ] 에러 코드 정의
- [ ] 버전 관리 전략 수립

### 구현 중

- [ ] 인증/인가 구현
- [ ] 입력값 검증
- [ ] 에러 처리
- [ ] 로깅 구현
- [ ] 캐싱 적용
- [ ] Rate Limiting
- [ ] CORS 설정

### 배포 전

- [ ] API 문서화 (OpenAPI/Swagger)
- [ ] 단위 테스트 (80%+)
- [ ] 통합 테스트
- [ ] 성능 테스트
- [ ] 보안 검토
- [ ] 모니터링 설정

## 💡 Best Practices

### DO ✅

1. **일관성 유지** - 동일한 패턴 사용
2. **명확한 이름** - 직관적인 엔드포인트
3. **적절한 상태 코드** - 의미에 맞는 코드 사용
4. **버전 관리** - 하위 호환성 유지
5. **문서화** - 항상 최신 상태 유지
6. **보안** - HTTPS, 인증, Rate Limiting
7. **테스트** - 충분한 테스트 커버리지

### DON'T ❌

1. ❌ URL에 동사 사용
2. ❌ 상태 관리 (Stateful)
3. ❌ 일관성 없는 명명
4. ❌ 과도한 중첩 (3단계 이상)
5. ❌ 에러 메시지 노출 (스택 트레이스)
6. ❌ 하드코딩된 값
7. ❌ 문서화 누락

## 🔗 추천 도구

### 개발 도구
- **Postman** - API 테스트
- **Swagger UI** - API 문서화
- **Insomnia** - API 클라이언트
- **curl** - 커맨드라인 테스트

### 문서화
- **OpenAPI** - API 스펙 표준
- **Redoc** - 문서 생성
- **Stoplight** - API 설계

### 모니터링
- **Datadog** - APM
- **New Relic** - 성능 모니터링
- **Sentry** - 에러 추적

## 📖 참고 자료

- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [API Design Guide (Google)](https://cloud.google.com/apis/design)

---

**업데이트:** 2026-03-07  
**버전:** 1.0  
**태그:** #api #rest #restful #api-design #web-development