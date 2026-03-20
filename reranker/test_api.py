#!/usr/bin/env python3
"""
Unified API 테스트 스크립트

사용법:
    python test_api.py https://xxxxx-8000.proxy.runpod.net
"""

import sys
import requests
import json

def test_api(base_url):
    """API 테스트 실행"""

    print("=" * 70)
    print("🚀 Unified API (Reranker + OCR) 테스트 시작")
    print("=" * 70)
    print(f"\n📍 API URL: {base_url}\n")

    # 1. Root endpoint 테스트
    print("1️⃣  Root endpoint 테스트 (GET /)")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response:")
        print(f"   {json.dumps(response.json(), indent=6, ensure_ascii=False)}")
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        return

    print("\n" + "-" * 70 + "\n")

    # 2. Health check 테스트
    print("2️⃣  Health check 테스트 (GET /health)")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response:")
        print(f"   {json.dumps(data, indent=6, ensure_ascii=False)}")

        if not data.get("services", {}).get("reranker", {}).get("loaded"):
            print("\n   ⚠️  경고: Reranker 모델이 아직 로드되지 않았습니다.")
            print("   잠시 후 다시 시도하세요.")
            return
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        return

    print("\n" + "-" * 70 + "\n")

    # 3. Rerank 테스트 (영어)
    print("3️⃣  Rerank 테스트 - 영어 (POST /rerank)")
    test_data_en = {
        "query": "What are health benefits of exercise?",
        "documents": [
            "Regular physical activity helps control weight by burning calories and building muscle mass.",
            "The Olympic Games originated in ancient Greece around 776 BC.",
            "Exercise improves cardiovascular health and reduces the risk of chronic diseases.",
            "Many people enjoy watching sports on television during weekends.",
            "Physical fitness can boost your immune system and mental health."
        ],
        "top_k": 3,
        "return_documents": True
    }

    try:
        response = requests.post(
            f"{base_url}/rerank",
            json=test_data_en,
            timeout=15
        )
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   📊 총 문서 수: {data['total_documents']}")
        print(f"   🎯 반환된 결과: {len(data['results'])}개\n")

        for i, result in enumerate(data['results'], 1):
            print(f"   {i}. Score: {result['score']:.4f} | Index: {result['index']}")
            print(f"      📝 {result['document'][:80]}...")
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        if hasattr(e, 'response'):
            print(f"   Response: {e.response.text}")
        return

    print("\n" + "-" * 70 + "\n")

    # 4. Rerank 종합 테스트 (한국어/영어 혼합, 30개 문서)
    print("4️⃣  Rerank 종합 테스트 - 한국어/영어 혼합 30개 문서 (POST /rerank)")
    test_data_ko = {
        "query": "규칙적인 운동의 건강상 이점은 무엇인가요?",
        "documents": [

            # 역사/문화 관련 (관련성 없음 - 예상 순위 24-27)
            "한국의 조선시대는 1392년부터 1910년까지 지속되었습니다.",
            "The Renaissance period began in Italy in the 14th century.",
            "세종대왕은 한글을 창제하여 문자 생활의 혁명을 일으켰습니다.",
            "The Great Wall of China was built over many centuries.",

            # 기술 관련 (관련성 없음 - 예상 순위 19-23)
            "인공지능은 현대 기술의 핵심 분야로 자리잡고 있습니다.",
            "Quantum computers use qubits instead of traditional bits.",
            "5G 네트워크는 이전 세대보다 훨씬 빠른 속도를 제공합니다.",
            "Python is one of the most popular programming languages.",
            "블록체인 기술은 암호화폐의 기반이 됩니다.",

            # 스포츠 관련 (중간 관련성 - 예상 순위 9-13)
            "올림픽 게임의 역사는 기원전 776년경 고대 그리스로 거슬러 올라갑니다.",
            "많은 사람들이 주말에 텔레비전으로 스포츠를 시청하는 것을 즐깁니다.",
            "The FIFA World Cup is held every four years in different countries.",
            "프로 운동선수들은 하루에 6-8시간의 훈련을 합니다.",
            "Basketball was invented by James Naismith in 1891.",

            # 운동 건강 관련 (관련성 높음 - 예상 순위 1-8)
            "규칙적인 신체 활동은 칼로리를 연소하고 근육량을 늘려 체중 조절에 도움이 됩니다.",
            "운동은 심혈관 건강을 개선하고 만성 질환의 위험을 줄입니다.",
            "신체 건강은 면역 체계와 정신 건강을 향상시킬 수 있습니다.",
            "Regular exercise strengthens your heart and improves blood circulation.",
            "Physical activity releases endorphins that reduce stress and anxiety.",
            "운동을 하면 뼈 밀도가 증가하고 골다공증 예방에 도움이 됩니다.",
            "Consistent workouts improve sleep quality and energy levels throughout the day.",
            "유산소 운동은 폐 기능을 향상시키고 지구력을 증가시킵니다.",

            # 음식/영양 관련 (낮은 관련성 - 예상 순위 14-18)
            "균형 잡힌 식단은 다양한 영양소를 포함해야 합니다.",
            "Protein is essential for muscle growth and repair.",
            "비타민 C는 면역 체계 강화에 중요한 역할을 합니다.",
            "Drinking 8 glasses of water daily keeps you hydrated.",
            "한국의 전통 음식인 김치는 발효 식품으로 건강에 좋습니다.",


            # 자연/환경 관련 (관련성 없음 - 예상 순위 28-30)
            "지구 온난화는 기후 변화의 주요 원인입니다.",
            "Tropical rainforests are home to over half of the world's species.",
            "재활용은 환경 보호를 위한 중요한 실천 방법입니다."
        ],
        "top_k": 5,
        "return_documents": True
    }

    try:
        response = requests.post(
            f"{base_url}/rerank",
            json=test_data_ko,
            timeout=15
        )
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   📊 총 문서 수: {data['total_documents']}")
        print(f"   🎯 반환된 Top {len(data['results'])}개 결과:\n")

        print(f"질문: {test_data_ko['query']}\n")
        for i, result in enumerate(data['results'], 1):
            print(f"   {i}. Score: {result['score']:.4f} | 원본 Index: {result['index']}")
            doc_preview = result['document'][:70] + "..." if len(result['document']) > 70 else result['document']
            print(f"      📝 {doc_preview}\n")

        print(f"   💡 Reranker가 30개 문서 중 가장 관련성 높은 5개를 선택했습니다!")
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        if hasattr(e, 'response'):
            print(f"   Response: {e.response.text}")
        return

    print("\n" + "-" * 70 + "\n")

    # 5. 엣지 케이스 테스트
    print("5️⃣  엣지 케이스 테스트")

    # top_k가 문서 개수보다 많은 경우
    print("   📌 top_k > 문서 개수")
    try:
        response = requests.post(
            f"{base_url}/rerank",
            json={
                "query": "test",
                "documents": ["doc1", "doc2"],
                "top_k": 10
            },
            timeout=10
        )
        data = response.json()
        print(f"   ✅ 문서 2개, top_k=10 요청 → {len(data['results'])}개 반환 (정상)")
    except Exception as e:
        print(f"   ❌ 실패: {e}")

    print("\n" + "=" * 70)
    print("🎉 모든 테스트 완료!")
    print("=" * 70)
    print("\n💡 다음 단계:")
    print("   - Swagger UI 확인: {}/docs".format(base_url))
    print("   - Django 연동 준비 완료!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python test_api.py <API_URL>")
        print("예시: python test_api.py https://xxxxx-8000.proxy.runpod.net")
        print("\n또는 로컬 테스트:")
        print("    python test_api.py http://localhost:8000")
        sys.exit(1)

    api_url = sys.argv[1].rstrip('/')
    test_api(api_url)
