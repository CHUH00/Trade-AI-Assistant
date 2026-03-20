# Unified API - Reranker + OCR

통합 AI API 서버: Document Reranker + OCR (추후 추가)

## 📋 현재 구현된 기능

- ✅ **Reranker** (mixedbread-ai/mxbai-rerank-large-v2)
- ⏳ **OCR** (추후 추가 예정)

## 🚀 빠른 시작

### 1. RunPod 배포

#### 1-1. Docker 이미지 빌드 & 푸시

```bash
cd /Users/hoon/Desktop/runpod/unified_api

# Docker Hub 로그인
docker login

# 이미지 빌드
docker build -t your-dockerhub-username/unified-api:latest .

# 이미지 푸시
docker push your-dockerhub-username/unified-api:latest
```

#### 1-2. RunPod 팟 생성

1. https://runpod.io 로그인
2. **Deploy** → **GPU Pod** 선택
3. **GPU 선택**: RTX 4090 또는 RTX 3090 추천
4. **Container Image**: `your-dockerhub-username/unified-api:latest`
5. **Container Port**: `8000`
6. **Expose HTTP Ports**: ✅ 체크
7. **Deploy** 클릭

#### 1-3. URL 확인

팟이 시작되면 URL 받음:
```
https://xxxxx-8000.proxy.runpod.net
```

### 2. 테스트

#### Swagger UI로 테스트 (가장 쉬움)
```
https://xxxxx-8000.proxy.runpod.net/docs
```

#### 테스트 스크립트 실행
```bash
python test_api.py https://xxxxx-8000.proxy.runpod.net
```

#### curl로 테스트
```bash
# Health check
curl https://xxxxx-8000.proxy.runpod.net/health

# Rerank
curl -X POST https://xxxxx-8000.proxy.runpod.net/rerank \
  -H "Content-Type: application/json" \
  -d '{
    "query": "운동의 이점",
    "documents": ["운동은 건강에 좋다", "날씨가 좋다"],
    "top_k": 5
  }'
```

---

## 📡 API 엔드포인트

### GET `/`
API 정보 및 사용 가능한 서비스 확인

**Response:**
```json
{
  "message": "Unified API - Reranker & OCR",
  "version": "1.0.0",
  "services": {
    "reranker": {
      "status": "available",
      "model": "mixedbread-ai/mxbai-rerank-large-v2"
    },
    "ocr": {
      "status": "coming soon"
    }
  }
}
```

### GET `/health`
서비스 헬스 체크

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "reranker": {
      "loaded": true,
      "status": "ready"
    }
  }
}
```

### POST `/rerank`
문서 리랭킹

**Request:**
```json
{
  "query": "검색 쿼리",
  "documents": ["문서1", "문서2", "문서3"],
  "top_k": 5,
  "return_documents": true
}
```

**Response:**
```json
{
  "results": [
    {
      "index": 0,
      "score": 0.95,
      "document": "문서1"
    }
  ],
  "query": "검색 쿼리",
  "total_documents": 3
}
```

---

## 🔗 Django 연동

### settings.py
```python
UNIFIED_API_URL = "https://xxxxx-8000.proxy.runpod.net"
```

### views.py
```python
import requests
from django.conf import settings

def rerank_documents(query, documents, top_k=5):
    """문서 리랭킹"""
    try:
        response = requests.post(
            f"{settings.UNIFIED_API_URL}/rerank",
            json={
                "query": query,
                "documents": documents,
                "top_k": top_k,
                "return_documents": True
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Reranker API 에러: {e}")
        return None

# 사용 예시
results = rerank_documents(
    query="사용자 검색어",
    documents=["문서1", "문서2", "문서3"],
    top_k=5
)

if results:
    for result in results['results']:
        print(f"Score: {result['score']}, Document: {result['document']}")
```

---

## 🛠 로컬 개발

### 요구사항
- Python 3.10+
- CUDA (GPU 사용 시)

### 설치
```bash
pip install -r requirements.txt
```

### 실행
```bash
python main.py
```

서버가 http://localhost:8000 에서 실행됩니다.

### 로컬 테스트
```bash
python test_api.py http://localhost:8000
```

---

## 📁 프로젝트 구조

```
unified_api/
├── main.py                      # FastAPI 앱 진입점
├── requirements.txt             # Python 의존성
├── Dockerfile                  # Docker 설정
├── test_api.py                 # API 테스트 스크립트
├── README.md                   # 배포 가이드
├── ARCHITECTURE.md             # 아키텍처 상세 설명 📖
│
├── models/                     # Pydantic 모델
│   ├── __init__.py
│   ├── reranker.py            ✅
│   └── ocr.py.template        (OCR 추가용)
│
├── services/                   # 비즈니스 로직
│   ├── __init__.py
│   ├── reranker.py            ✅
│   └── ocr.py.template        (OCR 추가용)
│
└── routers/                    # API 엔드포인트
    ├── __init__.py
    ├── reranker.py            ✅
    └── ocr.py.template        (OCR 추가용)
```

**모듈화된 구조의 장점:**
- 🔧 유지보수 쉬움
- 📈 확장성 우수
- 🧪 테스트 용이
- 📚 코드 가독성 향상

자세한 내용은 [ARCHITECTURE.md](ARCHITECTURE.md)를 참고하세요.

---

## 🔮 향후 추가 예정

### OCR 기능
```python
# POST /ocr (추후 추가)
{
  "image": "base64_encoded_image",
  "language": "ko"
}
```

OCR 기능 추가 시:
1. `main.py`에서 OCR 관련 주석 제거
2. OCR 모델 로딩 로직 추가
3. `requirements.txt`에 OCR 라이브러리 추가
4. Dockerfile 업데이트 (필요한 시스템 라이브러리)

---

## 🐛 트러블슈팅

### 문제 1: 503 Service Unavailable
→ 모델이 아직 로딩 중입니다. RunPod 로그 확인 후 "모델 로딩 완료" 메시지 대기

### 문제 2: 포트 접근 불가
→ RunPod 설정에서 "Expose HTTP Ports" 체크 확인

### 문제 3: Out of Memory
→ 더 큰 GPU 선택 (RTX 4090, A100 등)

### 문제 4: 느린 응답
→ GPU 선택 확인 (CPU 모드는 매우 느림)

---

## 💰 비용 최적화

- **사용하지 않을 때**: Stop Pod
- **필요할 때만**: Start Pod
- **GPU 선택**: RTX 3090 (~$0.34/hr) 또는 RTX 4090 (~$0.44/hr)
- **Spot vs On-Demand**: Spot이 저렴 (중단 위험 있음)

---

## 📞 지원

문제 발생 시:
1. RunPod 로그 확인
2. `/health` 엔드포인트 확인
3. `/docs`에서 Swagger UI로 직접 테스트
