"""Reranker 서비스 - 모델 로딩 및 비즈니스 로직"""

import logging
from typing import Optional
from mxbai_rerank import MxbaiRerankV2

logger = logging.getLogger(__name__)


class RerankerService:
    """Reranker 모델 관리 및 실행"""

    def __init__(self):
        self.model: Optional[MxbaiRerankV2] = None
        self.model_name = "mixedbread-ai/mxbai-rerank-large-v2"

    async def load_model(self):
        """모델을 로드합니다"""
        try:
            logger.info(f"🔄 Reranker 모델 로딩 시작: {self.model_name}")
            self.model = MxbaiRerankV2(self.model_name)
            logger.info("✅ Reranker 모델 로딩 완료")
        except Exception as e:
            logger.error(f"❌ Reranker 모델 로딩 실패: {str(e)}")
            self.model = None
            raise

    def is_ready(self) -> bool:
        """모델이 준비되었는지 확인"""
        return self.model is not None

    def rank(self, query: str, documents: list[str], top_k: int, return_documents: bool):
        """문서 리랭킹을 수행합니다"""
        if not self.is_ready():
            raise RuntimeError("Reranker 모델이 로드되지 않았습니다")

        # top_k 값이 문서 개수를 초과하지 않도록 조정
        actual_top_k = min(top_k, len(documents))

        # 리랭킹 수행
        results = self.model.rank(
            query,
            documents,
            return_documents=return_documents,
            top_k=actual_top_k
        )

        return results


# 전역 서비스 인스턴스 -> 로딩된 리랭커 모델 저장
reranker_service = RerankerService()
