import os
import cv2
import numpy as np
from facenet_pytorch import InceptionResnetV1, MTCNN
import mediapipe as mp
from PIL import Image
import chromadb
from chromadb import PersistentClient

def init_chroma_db():
    persist_directory = "{크로마DB 저장 경로}"
    client = PersistentClient(path=persist_directory)

    collection_name = "faces_nnnnn"
    try:
        db = client.get_collection(name=collection_name)  # 기존 컬렉션 가져오기
        print(f"Using existing ChromaDB collection '{collection_name}'")
    except ValueError:
        db = client.create_collection(name=collection_name)  # 없으면 새로 생성
        print(f"Created new ChromaDB collection '{collection_name}' in '{persist_directory}'")

    return db

# Initialize the face detection and recognition models
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)
model = InceptionResnetV1(pretrained='vggface2').eval()  # Always 512-dimensions
mtcnn = MTCNN(keep_all=False, device='cpu')

def extract_frames(video_path, interval=1):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames = []
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % (interval * fps) == 0:
            frames.append(frame)
        count += 1
    cap.release()
    return frames

def extract_face_vectors(frames):
    face_vectors = []
    for frame in frames:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = mp_face_mesh.process(rgb_frame)
        if face_locations.multi_face_landmarks:
            image_pil = Image.fromarray(rgb_frame)
            faces = mtcnn(image_pil)
            if faces is not None:
                face = faces.unsqueeze(0)
                embedding = model(face).detach().numpy()
                face_vectors.append(embedding.flatten())  # 512-dimensional vector
                
                # 첫 번째 얼굴 벡터만 저장하고 반복 중단
                return face_vectors
    return face_vectors

def save_face_vectors_to_chroma(db, face_vectors, video_title):
    for i, vector in enumerate(face_vectors):
        db.add(
            embeddings=[vector.tolist()],
            metadatas=[{"video_title": video_title}],
            ids=[f"{video_title}_{i}"]
        )

def is_video_already_processed(db, video_title):
    # 확장자 제거한 video_title을 사용하여 ChromaDB에 저장된 메타데이터 검색
    results = db.get(where={"video_title": video_title})  # video_title로 검색
    return len(results['documents']) > 0  # 이미 저장된 문서가 있으면 True 반환

def process_video(db, video_path, video_title):
    if is_video_already_processed(db, video_title):
        print(f"Video '{video_title}' is already processed. Skipping...")
        return
    
    try:
        frames = extract_frames(video_path, interval=10)
        face_vectors = extract_face_vectors(frames)
        save_face_vectors_to_chroma(db, face_vectors, video_title)
        print(f"Successfully processed video: {video_title}")
    except Exception as e:
        print(f"Error processing video {video_title}: {e}")

def process_videos_in_folder(db, folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
            video_path = os.path.join(folder_path, filename)
            video_title = os.path.splitext(filename)[0]  # 확장자를 제거한 파일명 사용
            print(f"Processing video: {video_title}")
            process_video(db, video_path, video_title)
    print("All videos processed.")

def check_data_in_chroma(db, video_title):
    # 512차원 벡터를 쿼리하는 샘플 코드 (fake embedding 사용)
    fake_embedding = np.zeros(512)  # 임의의 512차원 벡터 생성
    results = db.query(
        query_embeddings=[fake_embedding.tolist()],
        n_results=1
    )
    print(f"Query results: {results}")
    
    if results['documents']:
        print(f"Data for '{video_title}' is successfully stored.")
    else:
        print(f"No data found for '{video_title}'.")

# 컬렉션을 초기화하거나 기존 컬렉션을 가져옴
db = init_chroma_db()

# 비디오 파일이 있는 폴더 경로
folder_path = "{비디오 파일이 있는 폴더 경로}"
process_videos_in_folder(db, folder_path)

# 저장된 데이터를 확인
check_data_in_chroma(db, "{확인하고 싶은 영상 제목}")
