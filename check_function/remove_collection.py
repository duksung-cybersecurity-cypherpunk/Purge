from chromadb import PersistentClient

# ChromaDB 클라이언트 생성
persist_directory = "/Users/sinhyoseom/chroma_storage"
client = PersistentClient(path=persist_directory)

# 삭제할 컬렉션 이름
collection_name = "faces_nnnnn"

try:
    client.delete_collection(name=collection_name)
    print(f"Collection '{collection_name}' deleted successfully.")
except ValueError:
    print(f"Collection '{collection_name}' does not exist.")
