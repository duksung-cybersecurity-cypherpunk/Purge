Purge

requirements
Flask==2.2.5  
keras-facenet==0.3.2  
mtcnn==0.1.1  
facenet-pytorch==2.5.2  
chromadb==0.4.0  
mediapipe==0.9.1  
opencv-python==4.7.0.72  
Pillow==9.4.0  
numpy==1.24.3  
---
소개 
Purge는 얼굴 인식 및 데이터베이스 검색 기술을 활용하여 디지털 성범죄 피해자들이 유해 콘텐츠를 탐지하고 증거를 확보할 수 있도록 돕는 프로젝트입니다.

---
특징

1. 얼굴 인식 및 벡터화  
   - MTCNN을 사용하여 이미지를 분석하고 얼굴을 탐지합니다.  
   - FaceNet과 InceptionResnetV1으로 얼굴 특징을 512차원 벡터로 변환하여 유사도를 측정합니다.  

2. 유해 콘텐츠 탐지 및 검색  
   - ChromaDB를 사용하여 얼굴 벡터를 고속으로 검색하고, 유사 콘텐츠를 탐지합니다.  
   - 검색 결과는 메타데이터(예: URL, 제목)와 함께 제공됩니다.  

3. 비디오 분석  
   - OpenCV로 동영상 파일에서 간격별로 프레임을 추출하고 얼굴 데이터를 수집합니다.  
   - Mediapipe로 정밀한 얼굴 랜드마크를 탐지하여 얼굴 정보를 수집합니다.  

4. 결과 제공  
   - 매칭된 콘텐츠는 유사도 순으로 정렬되어 제공됩니다. 추가적으로 썸네일과 메타데이터를 통해 시각적 정보를 제공합니다.  

---
기술 스택 

- 프론트엔드: HTML, CSS, JavaScript (UI/UX)  
- 백엔드: Python (Flask)  
- 머신러닝 모델:  
  - MTCNN: 얼굴 탐지  
  - FaceNet 및 InceptionResnetV1: 얼굴 벡터화  
- 데이터베이스: ChromaDB  
- 영상 처리: OpenCV, Mediapipe  
- 데이터 저장소: PersistentClient (ChromaDB)  

---
설치 및 실행 방법

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
주요 파일 설명

1. 기본 파일
- index.html: 메인 페이지
- face_scan.html: 얼굴 스캔 페이지
- purge_page.html: 검색 결과 표시 페이지
- report_status.html: 신고 상태 페이지
- report_history.html: 신고 이력 페이지
- verification.html: 사용자 인증 페이지


2. realpurge
- app.py: Flask를 기반으로 한 애플리케이션 백엔드 로직

3. checkfunction
- video_to_chroma.py: 동영상에서 얼굴 데이터를 추출하고 ChromaDB에 저장
- remove_collection.py: ChromaDB에서 특정 컬렉션을 삭제

