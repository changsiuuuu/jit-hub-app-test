# JIT-Hub 웹 서비스 아키텍처 문서

> 작성자: 최진제 (웹 서비스 담당)
> 최종 수정: 2026-07-07

---

## 1. 서비스 개요

JIT-Hub는 날씨 · 교통 · 관광지 데이터를 API로 제공하는 데이터 허브 서비스입니다.
MSA(Microservice Architecture) 구조로 설계되어 각 API 도메인이 독립된 서비스와 DB를 가집니다.

---

## 2. 전체 아키텍처

```
브라우저 / 외부 클라이언트
        │
        ▼
  ┌─────────────┐
  │   Nginx     │  :8000 (외부 유일 진입점)
  │  (Gateway)  │
  └──────┬──────┘
         │ URL 경로 기반 라우팅
    ┌────┴──────────────────────────┐
    │         │           │         │
    ▼         ▼           ▼         ▼
 /auth/*   /api/v1/    /api/v2/  /api/v3/
 /static/     │            │         │
    │          ▼            ▼         ▼
    ▼      weather      traffic   tourist
 auth       :8002        :8003     :8004
 :8001        │            │         │
    │          ▼            ▼         ▼
    ▼      weather_db  traffic_db tourist_db
 auth_db
```

---

## 3. 컨테이너 구성 (총 9개)

| 컨테이너 | 역할 | 내부 포트 | 외부 포트 | 연결 DB |
|---------|------|---------|---------|--------|
| gateway (Nginx) | API Gateway / 정적 파일 서빙 | 80 | **8000** | - |
| auth-service | 회원 · API키 관리 | 8001 | 미노출 | auth_db |
| weather-service | 날씨 API | 8002 | 미노출 | weather_db |
| traffic-service | 교통 API | 8003 | 미노출 | traffic_db |
| tourist-service | 관광지 API | 8004 | 미노출 | tourist_db |
| auth-db | PostgreSQL | 5432 | 미노출 | - |
| weather-db | PostgreSQL | 5432 | 미노출 | - |
| traffic-db | PostgreSQL | 5432 | 미노출 | - |
| tourist-db | PostgreSQL | 5432 | 미노출 | - |

> 외부에 노출된 포트는 **8000 (Nginx) 하나뿐**

---

## 4. 서비스별 상세

### 4-1. Nginx (Gateway)

- 외부 요청을 URL 경로 기준으로 적절한 서비스로 프록시
- `/static/` 디렉토리는 Nginx가 직접 파일 서빙 (FastAPI 불필요)
- 설정 파일: `gateway/nginx.conf`

**라우팅 규칙**

| URL 패턴 | 프록시 대상 |
|---------|-----------|
| `/` | `/static/login.html` 리다이렉트 |
| `/static/*` | 정적 파일 직접 서빙 |
| `/auth/*` | auth-service:8001 |
| `/health` | auth-service:8001 |
| `/api/v1/*` | weather-service:8002 |
| `/api/v2/*` | traffic-service:8003 |
| `/api/v3/*` | tourist-service:8004 |

---

### 4-2. auth-service

**담당 기능**
- 회원가입 / 로그인 / JWT 토큰 발급
- API Key 발급 · 조회 · 삭제
- 내부 API 키 검증 엔드포인트 제공

**엔드포인트**

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/auth/signup` | 회원가입 |
| POST | `/auth/login` | 로그인 (JWT 반환) |
| GET | `/auth/me` | 내 정보 조회 |
| POST | `/auth/apikey` | API Key 발급 |
| GET | `/auth/apikey` | 내 API Key 목록 |
| DELETE | `/auth/apikey/{id}` | API Key 삭제 |
| GET | `/internal/verify` | API Key 유효성 검증 (서비스 간 내부 호출용) |

**DB 테이블**
- `users` : id, email, name, hashed_password, created_at
- `api_keys` : id, user_id, key_name, api_type, key, status, is_active, created_at

---

### 4-3. weather-service

**담당 기능**
- 지역 코드 + 날짜 범위로 날씨 데이터 조회

**엔드포인트**

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/v1/weather` | 날씨 조회 (region, start_date, end_date 필수) |
| GET | `/api/v1/weather/regions` | 지원 지역 코드 목록 |

**지원 지역 코드**

| 코드 | 지역 |
|-----|------|
| 11 | 서울 |
| 21 | 부산 |
| 22 | 대구 |
| 23 | 인천 |
| 24 | 광주 |
| 25 | 대전 |
| 39 | 제주 |

**DB 테이블**
- `weather` : id, region_code, region_name, date, temp_max, temp_min, humidity, precipitation, condition
- 시드 데이터: 2025-01-01 ~ 2026-12-31 (7개 지역 × 730일 = 약 5,110건)

---

### 4-4. traffic-service

**담당 기능**
- 지역 코드 + 교통 유형(버스/지하철)으로 노선 및 혼잡도 조회

**엔드포인트**

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/v2/traffic` | 교통 노선 조회 (region, type 필수) |

**파라미터**
- `type`: `bus` / `subway`

**DB 테이블**
- `traffic_routes` : id, region_code, region_name, type, route_name, start_stop, end_stop, congestion, interval_min
- 시드 데이터: 서울·부산·대구·인천·제주 총 20개 노선

---

### 4-5. tourist-service

**담당 기능**
- 지역·카테고리 기반 관광지 목록 조회
- 관광지 상세 정보 (위치, 이미지, 입장료, 성수기/비성수기, 운영시간)
- 이름 검색

**엔드포인트**

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/v3/tourist` | 관광지 목록 (region, category 선택) |
| GET | `/api/v3/tourist/{id}` | 관광지 상세 |
| GET | `/api/v3/tourist/search/` | 이름 검색 (name 필수) |

**카테고리**: 자연 / 문화 / 역사 / 테마파크

**DB 테이블**
- `tourists` : id, name, region_code, region_name, category, address, latitude, longitude, admission_fee, admission_info, peak_season, off_season, open_hours, image_url, description
- 시드 데이터: 서울·부산·제주·강원·경북 총 10개 관광지

---

## 5. API Key 검증 흐름 (서비스 간 통신)

weather / traffic / tourist 서비스는 auth DB에 직접 접근하지 않고
**auth-service의 내부 API를 통해서만** 키 유효성을 검증합니다.

```
클라이언트
    │  api_key 포함 요청
    ▼
Nginx → weather-service
              │
              │ GET http://auth-service:8001/internal/verify?api_key=xxx
              ▼
         auth-service
              │ { "valid": true, "api_type": "weather" }
              ▼
         weather-service → weather_db 조회 → 응답 반환
```

이 구조로 각 서비스는 **자신의 DB만 접근** → 서비스 간 DB 커플링 없음

---

## 6. 디렉토리 구조

```
jit-hub-app/
├── services/
│   ├── auth/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   └── routers/
│   │   │       ├── auth.py
│   │   │       └── internal.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── weather/          (동일 구조 + seed.py)
│   ├── traffic/          (동일 구조 + seed.py)
│   └── tourist/          (동일 구조 + seed.py)
├── gateway/
│   └── nginx.conf
├── static/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── mypage.html
│   └── api-usage.html
├── docker-compose.yml    (로컬 개발 전용)
└── docs/
    └── architecture.md   (현재 문서)
```

---

## 7. 모니터링 계획 (EKS 환경)

로컬 docker-compose 환경에는 모니터링 없음.
EKS 배포 시 아래 스택을 Helm Chart로 추가 예정:

| 도구 | 역할 | 설치 방법 |
|-----|------|---------|
| kube-prometheus-stack | Prometheus + Grafana + Alertmanager + node-exporter + kube-state-metrics | Helm |
| Loki + Promtail | 로그 수집 및 저장 | Helm (추후 추가) |
| Thanos | A/B 리전 메트릭 통합 | Helm (추후 추가) |

**kube-prometheus-stack으로 수집 가능한 메트릭**
- 노드(EC2) CPU / 메모리 / 디스크 사용량
- 파드별 CPU / 메모리 사용량
- 디플로이먼트 상태 (replica 수, 재시작 횟수 등)

ArgoCD Application으로 관리하여 GitOps 방식으로 모니터링 설정도 버전 관리.

---

## 8. 로컬 개발 실행 방법

```bash
# 최초 실행 (이미지 빌드 포함)
docker-compose up --build -d

# 재시작
docker-compose up -d

# DB 초기화 후 재시작
docker-compose down -v && docker-compose up --build -d

# 로그 확인
docker-compose logs -f auth-service
docker-compose logs -f weather-service

# 전체 종료
docker-compose down
```

**접속 URL**: `http://localhost:8000`
