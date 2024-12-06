import os
import numpy as np
from facenet_pytorch import InceptionResnetV1, MTCNN
import base64
import io
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory
import torch
from flask_cors import CORS
from chromadb import PersistentClient
from sklearn.metrics.pairwise import cosine_similarity

# Flask 서버 초기화
app = Flask(__name__)
CORS(app, resources={r"/upload-image": {"origins": "*"}})

# MTCNN 및 FaceNet 모델 초기화
mtcnn = MTCNN(keep_all=False, device='cpu')  # MTCNN 얼굴 탐지 모델
model = InceptionResnetV1(pretrained='vggface2').eval()  # FaceNet 얼굴 인식 모델

# ChromaDB 초기화
def init_chroma_db():
    persist_directory = "{크로마DB저장경로}"
    client = PersistentClient(path=persist_directory)
    collection_name = "faces_nnnnn"

    try:
        db = client.get_collection(name=collection_name)
        print(f"Loaded ChromaDB collection '{collection_name}' from '{persist_directory}'")
    except ValueError as e:
        print(f"Error loading collection '{collection_name}': {e}")
        db = None  # None으로 설정

    return db

# 얼굴 벡터 추출 함수 (MTCNN을 사용하여 얼굴 감지)
def extract_face_vector(image):
    """MTCNN을 사용하여 얼굴을 감지하고, FaceNet으로 벡터를 추출"""
    try:
        faces = mtcnn(image)  # 얼굴 탐지
        if faces is not None:
            print(f"Detected {faces.shape} face(s).")
            face = faces.unsqueeze(0)  # 배치 차원 추가
            embedding = model(face).detach().numpy().flatten()  # FaceNet으로 벡터 추출
            print(f"Extracted embedding dimension: {embedding.shape[0]}")  # 벡터 차원 출력
            return embedding
        else:
            print("No face detected.")
            return None
    except Exception as e:
        print(f"Error during face vector extraction: {e}")
        return None

# 얼굴 벡터 비교 함수
def find_matching_faces(db, face_vector, threshold=0.35):
    if face_vector.shape[0] != 512:
        print(f"Error: Extracted face vector has dimension {face_vector.shape[0]}, expected 512.")
        return []

    # ChromaDB 쿼리 수행 후 결과 출력
    results = db.query(
        query_embeddings=[face_vector.tolist()],
        n_results=10
    )
    
    matching_urls = set()
    for distance, metadata in zip(results['distances'][0], results['metadatas'][0]):
        similarity = 1 - distance  # 거리 값으로부터 유사도 계산

        if similarity >= threshold:
            matching_urls.add(metadata['video_title'])
            print(f"Similarity: {similarity}, URL: {metadata['video_title']}")

    if not matching_urls:
        return ["저장된 영상이 없습니다."]

    return list(matching_urls)

THUMBNAIL_FOLDER = "{썸네일 저장 경로}"

@app.route('/thumbnails/<filename>')
def serve_thumbnail(filename):
    return send_from_directory(THUMBNAIL_FOLDER, filename)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    db = init_chroma_db()
    if db is None:
        return jsonify({'status': 'error', 'message': 'Database initialization failed.'})

    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image part in request.'})

    file = request.files['image']
    try:
        image = Image.open(file)

        # RGBA(4채널)인 경우 RGB(3채널)로 변환
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        face_vector = extract_face_vector(image)  # 얼굴 벡터 추출 함수 호출

        if face_vector is not None:
            matching_urls = find_matching_faces(db, face_vector)  # 동일 인물 찾기
            if matching_urls:
                response = {
                    'status': 'success',
                    'matching_urls': matching_urls
                }
            else:
                response = {
                    'status': 'success',
                    'message': '저장된 영상이 없습니다.'
                }
        else:
            response = {
                'status': 'error',
                'message': 'No face detected in the image.'
            }

    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
