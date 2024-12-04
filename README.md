# Purge

얼굴 인식 및 데이터베이스 검색 기술을 활용하여 디지털 성범죄 피해자들이 유해 콘텐츠를 탐지하고 증거를 확보할 수 있도록 돕는 프로젝트

---
### 특징

1. 얼굴 인식 및 벡터화  
   - MTCNN을 사용하여 이미지를 분석하고 얼굴을 탐지합니다.  
   - FaceNet과 InceptionResnetV1으로 얼굴 특징을 512차원 벡터로 변환하여 유사도를 측정합니다.  

2. 유해 콘텐츠 탐지 및 검색  
   - ChromaDB를 사용하여 얼굴 벡터를 고속으로 검색하고, 유사 콘텐츠를 탐지합니다.  
   - 검색 결과는 메타데이터와 함께 제공됩니다.  

3. 비디오 분석  
   - OpenCV로 동영상 파일에서 간격별로 프레임을 추출하고 얼굴 데이터를 수집합니다.  
   - Mediapipe로 정밀한 얼굴 랜드마크를 탐지하여 얼굴 정보를 수집합니다.  

4. 결과 제공  
   - 매칭된 콘텐츠는 유사도 순으로 정렬되어 제공됩니다. 추가적으로 썸네일과 메타데이터를 통해 시각적 정보를 제공합니다.  

---
### 기술 스택

- 프론트엔드: HTML, CSS, JavaScript (UI/UX)  
- 백엔드: Python (Flask)  
- 머신러닝 모델:  
  - MTCNN: 얼굴 탐지  
  - FaceNet 및 InceptionResnetV1: 얼굴 벡터화  
- 데이터베이스: ChromaDB  
- 영상 처리: OpenCV, Mediapipe  
- 데이터 저장소: PersistentClient (ChromaDB)  

---
### 설치 및 실행 방법

1. 프로젝트 클론  
   - git clone https://github.com/your-username/purge.git
   - cd purge

2. 필수 Python 패키지 설치  
   - pip install -r requirements.txt

3. ChromaDB 초기화  
   - video_to_chroma.py 또는 관련 파일에서 ChromaDB 경로를 설정합니다.  

4. 애플리케이션 실행  
   - python app.py

5. 웹 브라우저 열기  
   - `http://127.0.0.1:5000`을 브라우저에 입력하여 접근합니다.  

---
### 주요 파일 설명

1. 기본 파일
- index.html: 메인 페이지로 JSON 파일 업로드 및 초기 페이지 이동 처리
- face_scan.html: 사용자 이미지를 업로드하거나 실시간 촬영하여 얼굴 데이터를 처리
- purge_page.html: 검색된 매칭 결과와 유사도를 표시하며, 관련 콘텐츠 정보를 제공
- report_status.html: 신고 처리 상태를 요약하고, 각 상태별 콘텐츠 수 표시
- report_history.html: 이전에 신고된 콘텐츠의 기록 확인
- verification.html: 사용자 ID와 비밀번호로 인증 수행
- app.py: Flask를 기반으로 이미지 업로드, 얼굴 벡터 추출, ChromaDB와의 매칭을 처리하는 애플리케이션 백엔드 로직

2. checkfunction
- video_to_chroma.py: 동영상에서 얼굴 데이터를 추출하고 ChromaDB에 저장
- remove_collection.py: ChromaDB에서 특정 컬렉션을 삭제

---
### requiremente

Flask==2.2.5  
keras-facenet==0.3.2  
mtcnn==0.1.1  
facenet-pytorch==2.5.2  
chromadb==0.4.0  
mediapipe==0.9.1  
opencv-python==4.7.0.72  
Pillow==9.4.0  
numpy==1.24.3
