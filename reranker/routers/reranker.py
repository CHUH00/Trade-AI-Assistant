"""Reranker API 라우터"""

import logging
from fastapi import APIRouter, HTTPException

from models.reranker import RerankRequest, RerankResponse, RerankResult
from services.reranker import reranker_service

logger = logging.getLogger(__name__)

# 라우터
router = APIRouter(
    prefix="/rerank",
    tags=["Reranker"]
)


@router.post("", response_model=RerankResponse)
def rerank(request: RerankRequest):
    """
    문서 리랭킹 엔드포인트

    주어진 쿼리와 문서 리스트를 기반으로 관련도 순으로 정렬합니다.
    CPU/GPU 집약적 작업이므로 동기 함수로 구현.
    """
    # 모델 로딩 확인
    if not reranker_service.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Reranker 모델이 아직 로드되지 않았습니다. 잠시 후 다시 시도해주세요."
        )

    # 입력 검증
    if not request.documents:
        raise HTTPException(
            status_code=400,
            detail="documents 리스트가 비어있습니다."
        )

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="query가 비어있습니다."
        )

    try:
        # 리랭킹 수행
        results = reranker_service.rank(
            query=request.query,
            documents=request.documents,
            top_k=request.top_k,
            return_documents=request.return_documents
        )

        # 결과 포맷팅
        formatted_results = []
        for result in results:
            formatted_result = {
                "index": result.index,
                "score": result.score,
            }
            if request.return_documents:
                formatted_result["document"] = result.document
            formatted_results.append(RerankResult(**formatted_result))

        return RerankResponse(
            results=formatted_results,
            query=request.query,
            total_documents=len(request.documents)
        )

    except HTTPException:
        # HTTPException은 그대로 전달
        raise
    except Exception as e:
        # 예상치 못한 에러만 500으로 처리
        logger.error(f"리랭킹 처리 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"리랭킹 처리 중 오류 발생: {str(e)}"
        )
