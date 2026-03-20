# 프로젝트 아키텍처

## 📁 프로젝트 구조

```
unified_api/
├── main.py                      # FastAPI 앱 진입점
├── requirements.txt             # Python 의존성
├── Dockerfile                  # Docker 설정
├── test_api.py                 # API 테스트 스크립트
│
├── models/                     # Pydantic 모델 (Request/Response)
│   ├── __init__.py
│   ├── reranker.py            # Reranker 모델 ✅
│   └── ocr.py.template        # OCR 모델 템플릿 (나중에 사용)
│
├── services/                   # 비즈니스 로직 & 모델 관리
│   ├── __init__.py
│   ├── reranker.py            # Reranker 서비스 ✅
│   └── ocr.py.template        # OCR 서비스 템플릿 (나중에 사용)
│
└── routers/                    # API 엔드포인트
    ├── __init__.py
    ├── reranker.py            # Reranker 라우터 ✅
    └── ocr.py.template        # OCR 라우터 템플릿 (나중에 사용)
```

## 🏗️ 레이어 구조

### 1. **main.py** - 애플리케이션 진입점
- FastAPI 앱 초기화
- 라우터 등록
- 서버 시작 이벤트 (모델 로딩)
- 기본 엔드포인트 (/, /health)

### 2. **routers/** - API 엔드포인트 레이어
- HTTP 요청/응답 처리
- 입력 검증
- 에러 핸들링
- 서비스 레이어 호출

### 3. **services/** - 비즈니스 로직 레이어
- AI 모델 로딩 및 관리
- 실제 비즈니스 로직 수행
- 모델 상태 관리

### 4. **models/** - 데이터 모델 레이어
- Pydantic 모델 정의
- Request/Response 스키마
- 데이터 검증 규칙

## 🔄 데이터 흐름

```
클라이언트 요청
    ↓
main.py (FastAPI 앱)
    ↓
routers/reranker.py (엔드포인트)
    ↓
services/reranker.py (비즈니스 로직)
    ↓
AI 모델 실행
    ↓
models/reranker.py (응답 포맷팅)
    ↓
클라이언트 응답
```

## ✨ 모듈화의 장점

### 1. **관심사의 분리 (Separation of Concerns)**
- 각 레이어가 명확한 책임을 가짐
- 수정 시 다른 부분에 영향 최소화

### 2. **유지보수성 향상**
- 버그 수정 시 해당 레이어만 수정
- 코드 위치를 쉽게 찾을 수 있음

### 3. **확장성**
- 새로운 서비스(OCR) 추가 시 템플릿 활용
- 기존 코드 수정 없이 기능 추가 가능

### 4. **테스트 용이성**
- 각 레이어를 독립적으로 테스트 가능
- Mock 객체로 서비스 레이어 테스트 가능

### 5. **재사용성**
- 서비스 로직을 다른 엔드포인트에서도 사용 가능
- 모델 정의를 여러 곳에서 공유 가능

## 🔮 OCR 추가 방법

### 1단계: 템플릿 파일 이름 변경
```bash
mv models/ocr.py.template models/ocr.py
mv services/ocr.py.template services/ocr.py
mv routers/ocr.py.template routers/ocr.py
```

### 2단계: models/__init__.py 업데이트
```python
from .reranker import RerankRequest, RerankResult, RerankResponse
from .ocr import OCRRequest, OCRResponse  # 추가

__all__ = [
    "RerankRequest", "RerankResult", "RerankResponse",
    "OCRRequest", "OCRResponse",  # 추가
]
```

### 3단계: services/__init__.py 업데이트
```python
from .reranker import RerankerService
from .ocr import OCRService  # 추가

__all__ = ["RerankerService", "OCRService"]  # 추가
```

### 4단계: routers/__init__.py 업데이트
```python
from .reranker import router as reranker_router
from .ocr import router as ocr_router  # 추가

__all__ = ["reranker_router", "ocr_router"]  # 추가
```

### 5단계: main.py에서 주석 제거
```python
# OCR 관련 주석 제거하고 활성화
from services.ocr import ocr_service
from routers import ocr_router

# 모델 로딩
await ocr_service.load_model()

# 라우터 등록
app.include_router(ocr_router)
```

### 6단계: requirements.txt에 OCR 라이브러리 추가
```
# OCR 라이브러리 추가 (예시)
easyocr==1.7.0
# 또는
paddleocr==2.7.0
```

## 🎯 현재 상태

### ✅ 완료된 부분
- [x] Reranker 서비스 완전 구현
- [x] 모듈화된 구조
- [x] 에러 핸들링
- [x] 로깅
- [x] Health check
- [x] API 문서 (Swagger)

### ⏳ 준비된 부분
- [x] OCR 템플릿 파일
- [x] 확장 가능한 구조
- [x] 명확한 추가 가이드

## 📝 코딩 컨벤션

### 파일명
- 소문자 + 언더스코어: `reranker.py`, `ocr.py`
- 템플릿 파일: `.template` 확장자 추가

### 클래스명
- PascalCase: `RerankerService`, `OCRService`
- Pydantic 모델: `RerankRequest`, `OCRResponse`

### 함수명
- snake_case: `load_model()`, `is_ready()`

### 로깅
- 이모지 활용: 🔄 (로딩), ✅ (성공), ❌ (실패)
- 명확한 메시지

## 🚀 배포

모듈화된 구조는 Docker 이미지 크기나 배포 방식에 영향 없음.
모든 모듈이 함께 패키징되어 배포됩니다.
