# RunPod 배포 가이드 (완전판)

> **전체 과정:** Docker 이미지 빌드 → Docker Hub 푸시 → RunPod 배포

---

## 🐳 0단계: Docker 이미지 빌드 & 푸시

### 0-1. 준비사항

**필수:**
- [ ] Docker Desktop 설치됨
- [ ] Docker Hub 계정 (https://hub.docker.com)
- [ ] 계정 사용자명 확인 (예: `hooncker`)

**로그인 확인:**
```bash
docker login
# 이미 로그인되어 있으면: Login Succeeded
```

---

### 0-2. 프로젝트 폴더로 이동

```bash
cd /Users/hoon/Desktop/runpod/unified_api
```

**현재 위치 확인:**
```bash
ls
# 확인할 파일: Dockerfile, main.py, requirements.txt
```

---

### 0-3. Docker 이미지 빌드

```bash
# 형식: docker build -t 사용자명/이미지명:태그 .
docker build -t hooncker/unified-api:latest .
```

**실행 예시:**
```bash
docker build -t hooncker/unified-api:latest .
```

**예상 출력:**
```
[+] Building 24.4s (10/10) FINISHED
 => [1/6] FROM python:3.10-slim
 => [2/6] WORKDIR /app
 => [3/6] RUN apt-get update && apt-get install...
 => [4/6] COPY requirements.txt .
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt
 => [6/6] COPY . .
 => naming to docker.io/hooncker/unified-api:latest
```

**⏱️ 예상 시간:**
- 첫 빌드: 20-30분 (PyTorch 다운로드 포함)
- 코드만 변경 후 재빌드: 1-2분 (캐시 사용)

---

### 0-4. 빌드 확인

```bash
docker images | grep unified-api
```

**예상 출력:**
```
hooncker/unified-api   latest   21a1300c8945   2 minutes ago   920MB
```

**✅ 확인사항:**
- 이미지명: `hooncker/unified-api`
- 태그: `latest`
- 크기: 약 920MB

---

### 0-5. Docker Hub에 푸시

```bash
docker push hooncker/unified-api:latest
```

**예상 출력:**
```
The push refers to repository [docker.io/hooncker/unified-api]
28eb9ccbc01e: Pushed
79cd91d652a0: Pushed
...
latest: digest: sha256:465d9a08... size: 2205
```

**⏱️ 예상 시간:** 5-15분 (인터넷 속도에 따라)

---

### 0-6. Docker Hub에서 확인

1. https://hub.docker.com 접속
2. 로그인
3. **Repositories** 탭
4. `unified-api` 찾기

**확인할 것:**
- ✅ 이미지가 보임
- ✅ `latest` 태그 있음
- ✅ **Public** 상태 (중요!)

---

### 🔧 문제 해결

#### 문제 1: `torch==2.8.0+cu128` 에러
```
ERROR: Could not find a version that satisfies the requirement torch==2.8.0+cu128
```

**해결:** requirements.txt 확인
```python
# ✅ 정확한 내용
torch>=2.0.0

# ❌ 잘못된 예
torch==2.8.0+cu128
```

#### 문제 2: Docker 로그인 안 됨
```
denied: requested access to the resource is denied
```

**해결:**
```bash
docker login
# Username: hooncker
# Password: (Docker Hub 비밀번호)
```

#### 문제 3: 사용자명 불일치
```bash
# ❌ 빌드: docker build -t hoocker/unified-api:latest .
# ✅ 로그인: hooncker

# 해결: 다시 태그
docker tag hoocker/unified-api:latest hooncker/unified-api:latest
docker push hooncker/unified-api:latest
```

---

### 📝 빠른 명령어 체크리스트

```bash
# 1. 프로젝트 이동
cd /Users/hoon/Desktop/runpod/unified_api

# 2. 빌드
docker build -t hooncker/unified-api:latest .

# 3. 확인
docker images | grep unified-api

# 4. 푸시
docker push hooncker/unified-api:latest

# 5. 정리 (선택)
docker system prune -a
```

---

## 📋 1단계: 배포 준비 확인

### ✅ 완료된 것들
- [x] Docker 이미지 빌드 완료
- [x] Docker Hub에 푸시 완료: `hooncker/unified-api:latest`
- [x] 이미지 크기: ~920MB
- [x] PyTorch 2.9.1 포함 (CUDA 자동 감지)
- [x] 이미지 Public 상태 확인

### 🔍 확인 필요
- [ ] RunPod 계정 (https://runpod.io)
- [ ] 크레딧 최소 $5 이상

---

## 🚀 2단계: RunPod에서 팟(Pod) 생성

### 2-1. RunPod 접속
1. https://runpod.io 로그인
2. 좌측 메뉴 → **Pods** 클릭
3. 우측 상단 → **+ Deploy** 버튼

### 2-2. 템플릿 선택
화면에 여러 템플릿이 보이면:

```
❌ Runpod Pytorch 2.8.0 (선택하지 마세요!)
✅ 아래로 스크롤해서 직접 입력
```

**"Change Template"** 또는 **"Custom"** 찾기

### 2-3. 컨테이너 설정 (중요!)

**Container Image 입력:**
```
hooncker/unified-api:latest
```

**Docker Command (선택):**
```
비워두기 (Dockerfile의 CMD 사용됨)
```

---

## ⚙️ 3단계: 팟 설정

### 필수 설정 ⭐

| 항목 | 값 | 설명 |
|-----|----|----|
| **Container Image** | `hooncker/unified-api:latest` | 필수! |
| **Expose HTTP Ports** | ✅ 체크 | 매우 중요! |
| **HTTP Port** | `8000` | 포트 번호 |
| **Container Disk** | `30 GB` | 모델 다운로드 공간 |

### 선택 설정

| 항목 | 추천 값 | 설명 |
|-----|--------|-----|
| **GPU Count** | `1` | Reranker는 1개면 충분 |
| **Pod Name** | 아무거나 | (자동 생성됨) |

### 가격 선택

**Spot (저렴):**
- 가격: ~$0.95/시간
- 중단될 수 있음 (드물게)
- 개발/테스트에 적합

**On-Demand (안정):**
- 가격: ~$1.49/시간
- 중단 없음
- 프로덕션에 적합

---

## 🎬 4단계: 배포 시작

### 4-1. 설정 최종 확인
```
✅ Container Image: hooncker/unified-api:latest
✅ Expose HTTP Ports: 체크됨
✅ HTTP Port: 8000
✅ Container Disk: 30GB
```

### 4-2. Deploy 클릭
우측 하단 **"Deploy"** 버튼 클릭

### 4-3. 대기 (1-2분)
팟 상태가 다음과 같이 변경됨:
```
Pending → Starting → Running
```

---

## 🌐 5단계: URL 확인 및 접속

### 5-1. URL 복사

팟이 **Running** 상태가 되면:

1. 팟 카드에서 **"Connect"** 버튼 클릭
2. **HTTP Service [Port 8000]** 찾기
3. URL 복사 (형식: `https://xxxxx-8000.proxy.runpod.net`)

### 5-2. 로그 확인 (중요!)

**"Logs"** 버튼 클릭 → 다음 메시지 확인:

```bash
INFO:     서버 시작 중...
INFO:     🔄 Reranker 모델 로딩 시작: mixedbread-ai/mxbai-rerank-large-v2
...
INFO:     ✅ Reranker 모델 로딩 완료
INFO:     ✅ 서버 준비 완료 V
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**⏱️ 예상 시간:**
- 첫 실행: 3-5분 (모델 다운로드)
- 이후: 30초-1분

**⚠️ 주의:** 로그에 "서버 준비 완료" 나올 때까지 기다리세요!

---

## 🧪 6단계: API 테스트

### 방법 1: 브라우저 (가장 쉬움)

**Health Check:**
```
https://xxxxx-8000.proxy.runpod.net/health
```

**예상 응답:**
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

### 방법 2: Swagger UI (추천!)

브라우저에서 접속:
```
https://xxxxx-8000.proxy.runpod.net/docs
```

**테스트 방법:**
1. **POST /rerank** 클릭
2. **Try it out** 클릭
3. **Execute** 클릭
4. 결과 확인!

### 방법 3: 테스트 스크립트

터미널에서:
```bash
cd /Users/hoon/Desktop/runpod/unified_api
python test_api.py https://xxxxx-8000.proxy.runpod.net
```

### 방법 4: curl

```bash
curl https://xxxxx-8000.proxy.runpod.net/health
```

---

## 🔗 7단계: Django 연동

### settings.py
```python
# 당신의 RunPod URL로 변경
RUNPOD_API_URL = "https://xxxxx-8000.proxy.runpod.net"
```

### views.py (사용 예시)
```python
import requests
from django.conf import settings

def search_with_rerank(query, initial_results):
    """검색 결과를 AI로 재정렬"""

    # 문서 리스트 추출
    documents = [result['content'] for result in initial_results]

    # Reranker API 호출
    response = requests.post(
        f"{settings.RUNPOD_API_URL}/rerank",
        json={
            "query": query,
            "documents": documents,
            "top_k": 10,
            "return_documents": True
        },
        timeout=10
    )

    if response.status_code == 200:
        return response.json()['results']
    else:
        # 에러 시 원본 결과 반환
        return initial_results
```

---

## 💰 8단계: 비용 관리

### 팟 정지 (사용 안 할 때)
```
Pods → 당신의 팟 → "Stop" 버튼
→ 과금 멈춤 ✅
```

### 팟 재시작 (다시 사용할 때)
```
Pods → 당신의 팟 → "Start" 버튼
→ 1-2분 대기 → URL 동일하게 사용 가능
```

### 팟 삭제 (완전 종료)
```
Pods → 당신의 팟 → "Terminate" 버튼
→ 완전 삭제 (URL도 사라짐)
```

### 비용 예시

| 사용 패턴 | GPU | 시간 | 비용 |
|----------|-----|------|------|
| 개발 (하루 4시간) | RTX 4090 Spot | 월 120시간 | ~$114/월 |
| 테스트 (필요시만) | RTX 4090 Spot | 월 20시간 | ~$19/월 |
| 24/7 운영 | RTX 4090 On-Demand | 월 720시간 | ~$1,073/월 |

**💡 Tip:** 개발 중엔 **Stop/Start 자주 사용**해서 비용 절감!

---

## 🐛 자주 발생하는 문제

### 문제 1: 503 Service Unavailable
```
원인: 모델이 아직 로딩 중
해결: 로그에서 "서버 준비 완료" 확인 (3-5분 대기)
```

### 문제 2: 포트 접근 불가
```
원인: "Expose HTTP Ports" 체크 안 함
해결: 팟 삭제 → 다시 생성 (이번엔 체크!)
```

### 문제 3: "Image not found"
```
원인: 이미지명 오타 또는 Private 설정
해결 1: hooncker/unified-api:latest 정확히 입력
해결 2: Docker Hub에서 이미지 Public 확인
```

### 문제 4: Out of Memory
```
원인: GPU 메모리 부족 (드물음)
해결: RTX 4090 이상 선택
```

---

## 📝 빠른 체크리스트

### 배포 전 ✅
- [ ] Docker Hub에 이미지 있음 (`hooncker/unified-api:latest`)
- [ ] RunPod 계정 로그인됨
- [ ] 크레딧 있음 ($5 이상)

### 배포 중 ⚙️
- [ ] Container Image: `hooncker/unified-api:latest`
- [ ] Expose HTTP Ports: **체크됨** ⭐
- [ ] HTTP Port: `8000`
- [ ] Container Disk: `30 GB`
- [ ] Deploy 버튼 클릭

### 배포 후 🧪
- [ ] 팟 상태: **Running**
- [ ] 로그에 "✅ 서버 준비 완료" 표시
- [ ] `/health` 엔드포인트 200 응답
- [ ] `/docs` 접속 가능
- [ ] Rerank 테스트 성공

---

## 🎯 다음 단계

### 현재 완료된 것
- ✅ Reranker API 배포 완료
- ✅ GPU에서 실행 중
- ✅ Django 연동 준비 완료

### 추가할 수 있는 기능
- [ ] OCR 서비스 추가 (템플릿 파일 활용)
- [ ] 모니터링 설정
- [ ] 로드 밸런싱 (여러 팟)

자세한 내용은 [ARCHITECTURE.md](ARCHITECTURE.md) 참고

---

## 🆘 도움이 필요하면

1. **RunPod 로그 확인** (가장 중요!)
2. **Swagger UI에서 직접 테스트** (`/docs`)
3. **Health check 먼저** (`/health`)

**잘 작동하면:** Django와 연동하고 실제 데이터로 테스트!

---

## 📊 배포 완료 확인

다음이 모두 작동하면 성공:

```bash
# 1. Health check
curl https://your-pod-url/health

# 2. Root endpoint
curl https://your-pod-url/

# 3. Rerank test
curl -X POST https://your-pod-url/rerank \
  -H "Content-Type: application/json" \
  -d '{
    "query": "운동의 이점",
    "documents": ["운동은 건강에 좋다", "날씨가 좋다"],
    "top_k": 5
  }'
```

모두 200 응답 → **배포 완료!** 🎉
