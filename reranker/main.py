"""
Unified API - Reranker + OCR

통합 AI API 서버
"""

import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1" # 모델 로드 빠르게 하게 해줌 (필수)

import logging
from fastapi import FastAPI

from routers import reranker_router
from services.reranker import reranker_service

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Unified API - Reranker & OCR",
    description="통합 AI API: Document Reranker + OCR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==================== 시작 이벤트 ====================

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 모델들을 로드합니다"""
    logger.info("서버 시작 중...")

    # Reranker 모델 로딩
    try:
        await reranker_service.load_model()
    except Exception as e:
        logger.error(f"Reranker 모델 로딩 실패: {e}")

    # OCR 모델 로딩 (나중에 추가)
    # try:
    #     await ocr_service.load_model()
    # except Exception as e:
    #     logger.error(f"OCR 모델 로딩 실패: {e}")

    logger.info("서버 준비 완료 V")


# ==================== 라우터 등록 ====================

# Reranker 라우터
app.include_router(reranker_router)

# OCR 라우터 (나중에 추가)
# app.include_router(ocr_router)


# ==================== 기본 엔드포인트 ====================

@app.get("/")
async def root():
    """API 정보 반환"""
    return {
        "message": "Unified API - Reranker & OCR",
        "version": "1.0.0",
        "services": {
            "reranker": {
                "status": "available" if reranker_service.is_ready() else "loading",
                "model": "mixedbread-ai/mxbai-rerank-large-v2",
                "endpoint": "/rerank"
            },
            "ocr": {
                "status": "coming soon",
                "endpoint": None
            }
        },
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "services": {
            "reranker": {
                "loaded": reranker_service.is_ready(),
                "status": "ready" if reranker_service.is_ready() else "not loaded"
            }
            # "ocr": {
            #     "loaded": ocr_service.is_ready(),
            #     "status": "ready" if ocr_service.is_ready() else "not loaded"
            # }
        }
    }


# ==================== 서버 실행 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
