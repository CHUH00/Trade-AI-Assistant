# RunPod SSH 배포 가이드 (Docker 없이)

**Docker 필요 없음! SSH로 바로 배포하기**

---

## 🚀 빠른 배포 (5분 완료)

### 1단계: RunPod 팟 생성

#### 1-1. RunPod 로그인
https://runpod.io 접속 및 로그인

#### 1-2. GPU Pod 생성
1. 좌측 메뉴 **Pods** 클릭
2. **+ Deploy** 클릭
3. GPU 선택: **RTX 4090** 또는 **RTX 3090**

#### 1-3. 템플릿 선택
**템플릿 검색에서:**
- `PyTorch` 검색
- **RunPod PyTorch** 또는 **RunPod Pytorch 2.x.x** 선택

**또는:**
- `Python` 검색
- 아무 Python 3.10+ 템플릿 선택

#### 1-4. 설정
- **Expose TCP Ports**: `8000` 입력 ✅
- **Volume Disk**: 기본값
- **Deploy** 클릭

---

### 2단계: SSH 접속

#### 2-1. SSH 정보 확인
팟이 **Running** 상태가 되면:
1. 팟 카드에서 **Connect** 버튼 클릭
2. **TCP Port Mappings** 섹션에서:
   - **Port 22 (SSH)** 정보 확인
   - **Port 8000** URL 확인 및 복사 (나중에 사용)

**SSH 접속 명령 예시:**
```
ssh root@xxx.xxx.xxx.xxx -p 12345 -i ~/.ssh/id_ed25519
```

#### 2-2. SSH 접속
**방법 1: RunPod에서 제공하는 명령어 복사**
```bash
# RunPod에서 복사한 SSH 명령어 그대로 실행
ssh root@xxx.xxx.xxx.xxx -p 12345 -i ~/.ssh/id_ed25519
```

**방법 2: 비밀번호 방식 (SSH 키 없는 경우)**
```bash
ssh root@xxx.xxx.xxx.xxx -p 12345
# 비밀번호: RunPod에서 표시됨
```

**접속 성공 시:**
```
root@xxxxx:~#
```

---

### 3단계: 프로젝트 업로드

#### 방법 A: Git 사용 (추천)

**3-1. GitHub에 프로젝트 업로드 (로컬에서)**
```bash
cd /Users/hoon/Desktop/runpod/unified_api

# Git 초기화 (처음 한 번만)
git init
git add .
git commit -m "Initial commit"

# GitHub에 푸시 (본인 레포지토리)
git remote add origin https://github.com/your-username/unified-api.git
git push -u origin main
```

**3-2. RunPod에서 Clone (SSH 접속 후)**
```bash
cd /workspace

# 본인 레포지토리 클론
git clone https://github.com/your-username/unified-api.git

cd unified-api
```

#### 방법 B: SCP로 직접 전송 (Git 없이)

**로컬 터미널에서:**
```bash
cd /Users/hoon/Desktop/runpod

# RunPod로 파일 전송 (포트와 주소는 RunPod에서 확인)
scp -P 12345 -r unified_api root@xxx.xxx.xxx.xxx:/workspace/
```

**RunPod SSH에서:**
```bash
cd /workspace/unified_api
```

---

### 4단계: 의존성 설치 (RunPod SSH에서)

```bash
# Python 버전 확인
python --version  # Python 3.10 이상이어야 함

# pip 업그레이드
pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt
```

**예상 시간:** 3-5분

**출력 예시:**
```
Collecting fastapi==0.121.2
Collecting uvicorn[standard]==0.38.0
...
Successfully installed fastapi-0.121.2 uvicorn-0.38.0 ...
```

---

### 5단계: 서버 실행

#### 방법 A: 간단 실행 (테스트용) ⭐ 추천
```bash
python main.py
```

**출력 예시:**
```
🚀 서버 시작 중...
🔄 Reranker 모델 로딩 시작: mixedbread-ai/mxbai-rerank-large-v2
...
✅ Reranker 모델 로딩 완료
✅ 서버 준비 완료
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**장점:**
- 로그가 바로 보임
- 간단함
- 테스트하기 좋음

**주의:**
- SSH 연결 끊으면 서버 종료됨
- 테스트 후 Ctrl+C로 종료

---

#### 방법 B: 백그라운드 실행 (장기 운영용)
```bash
# nohup으로 백그라운드 실행
nohup python main.py > server.log 2>&1 &

# 프로세스 ID 확인
echo $!
```

**장점:**
- SSH 끊어도 계속 실행됨 ⭐
- 서버 장기 운영 가능

**로그 확인:**
```bash
tail -f server.log
```

---

#### 방법 C: screen 사용 (가장 편리) ⭐⭐
```bash
# screen 세션 시작
screen -S api_server

# 서버 실행
python main.py

# Ctrl + A, 그 다음 D 로 detach (서버는 계속 실행됨)
```

**장점:**
- SSH 끊어도 계속 실행됨
- 언제든 다시 접속 가능
- 로그 실시간 확인 가능

**다시 접속:**
```bash
screen -r api_server
```

**종료:**
```bash
# screen 안에서
Ctrl + C  # 서버 종료
exit      # screen 종료
```

#### 방법 선택 가이드

| 상황 | 추천 방법 |
|------|----------|
| **처음 테스트** | 방법 A (python main.py) ⭐ |
| **계속 켜두기** | 방법 C (screen) ⭐⭐ |
| **자동화 스크립트** | 방법 B (nohup) |

**대부분의 경우 방법 C (screen)를 추천합니다!**

---

### 6단계: 테스트

#### 6-1. RunPod 내부에서 테스트
```bash
# SSH 접속 상태에서
curl http://localhost:8000/health
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

#### 6-2. 외부에서 테스트

**RunPod Port 8000 URL 확인:**
1. RunPod 웹사이트에서 팟 카드 확인
2. **TCP Port Mappings** → **Port 8000**의 외부 URL 복사

**URL 형식:**
```
https://xxxxx-8000.proxy.runpod.net
```

**로컬 터미널에서 테스트:**
```bash
cd /Users/hoon/Desktop/runpod/unified_api

python test_api.py https://xxxxx-8000.proxy.runpod.net
```

**브라우저에서 테스트:**
```
https://xxxxx-8000.proxy.runpod.net/docs
```

---

## 🔄 서버 관리

### 서버 중지
```bash
# 프로세스 찾기
ps aux | grep python

# 프로세스 종료 (PID는 위에서 확인)
kill <PID>

# 또는 모든 Python 프로세스 종료
pkill -f "python main.py"
```

### 서버 재시작
```bash
# 서버 중지 후
nohup python main.py > server.log 2>&1 &
```

### screen 세션 관리
```bash
# 세션 목록 보기
screen -ls

# 세션 재접속
screen -r api_server

# 세션 종료 (세션 안에서)
exit
```

---

## 🔧 코드 업데이트

### Git 사용 시
```bash
cd /workspace/unified_api

# 최신 코드 받기
git pull origin main

# 서버 재시작
pkill -f "python main.py"
nohup python main.py > server.log 2>&1 &
```

### SCP 사용 시
```bash
# 로컬에서 파일 재전송
scp -P 12345 /Users/hoon/Desktop/runpod/unified_api/main.py root@xxx.xxx.xxx.xxx:/workspace/unified_api/

# RunPod SSH에서 서버 재시작
pkill -f "python main.py"
nohup python main.py > server.log 2>&1 &
```

---

## 💰 비용 관리

### 팟 정지 (SSH 접속 끊고)
1. RunPod 웹사이트
2. 팟 카드에서 **Stop** 클릭
3. 파일은 보존됨 (Volume 사용 시)

### 팟 재시작
1. **Start** 클릭
2. SSH 재접속
3. 서버 재실행:
```bash
cd /workspace/unified_api
nohup python main.py > server.log 2>&1 &
```

---

## 📝 자동 시작 스크립트

**start_server.sh 생성:**
```bash
cat > /workspace/unified_api/start_server.sh << 'EOF'
#!/bin/bash
cd /workspace/unified_api
nohup python main.py > server.log 2>&1 &
echo "Server started! PID: $!"
tail -f server.log
EOF

chmod +x /workspace/unified_api/start_server.sh
```

**사용:**
```bash
./start_server.sh
```

---

## 🆚 Docker vs SSH 비교

| | Docker 방식 | SSH 방식 (현재) |
|---|---|---|
| **난이도** | 복잡 | 간단 ⭐ |
| **배포 시간** | 20-30분 | 5-10분 ⭐ |
| **코드 수정** | 재빌드 필요 | 바로 반영 ⭐ |
| **디버깅** | 어려움 | 쉬움 ⭐ |
| **재현성** | 높음 ⭐ | 보통 |
| **프로덕션** | 권장 ⭐ | 개발/테스트용 |

**결론:**
- **개발/테스트**: SSH 방식 (빠르고 간편)
- **프로덕션**: Docker 방식 (안정적)

---

## 🐛 트러블슈팅

### 문제 1: SSH 접속 안 됨
**해결:**
- RunPod에서 팟이 Running 상태인지 확인
- 포트와 주소 다시 확인

### 문제 2: Port 8000 접근 안 됨
**해결:**
- RunPod 팟 생성 시 "Expose TCP Ports: 8000" 설정했는지 확인
- 서버가 0.0.0.0:8000으로 실행되는지 확인

### 문제 3: 모듈을 찾을 수 없음
```bash
ModuleNotFoundError: No module named 'fastapi'
```
**해결:**
```bash
pip install -r requirements.txt
```

### 문제 4: 팟 재시작 후 서버 안 돌아감
**해결:**
- 서버는 자동 시작 안 됨
- SSH 재접속 후 수동으로 시작:
```bash
cd /workspace/unified_api
nohup python main.py > server.log 2>&1 &
```

---

## ✅ 체크리스트

- [ ] RunPod 팟 생성 (PyTorch 템플릿)
- [ ] Expose TCP Ports: 8000 설정 ✅
- [ ] SSH 접속 성공
- [ ] 프로젝트 파일 업로드 (Git 또는 SCP)
- [ ] `pip install -r requirements.txt` 완료
- [ ] `python main.py` 실행
- [ ] 로그에 "모델 로딩 완료" 확인
- [ ] 외부 URL로 테스트 성공
- [ ] Django 연동 테스트

---

## 🎉 완료!

**이제 Docker 없이 RunPod에서 API가 실행 중입니다!**

**다음 단계:**
- Django에서 RunPod URL 사용
- 필요 시 코드 수정 → `git pull` → 서버 재시작

**장점:**
- ✅ 빠른 배포 (5분)
- ✅ 쉬운 디버깅
- ✅ 즉시 코드 수정 가능
