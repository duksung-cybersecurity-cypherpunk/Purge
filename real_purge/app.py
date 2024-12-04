import os
import json
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from keras_facenet import FaceNet
from mtcnn import MTCNN
from PIL import Image
import webbrowser
from threading import Timer
from urllib.parse import unquote 

app = Flask(__name__)

detector = MTCNN()
embedder = FaceNet()
stored_vectors = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_json', methods=['POST'])
def upload_json():
    if 'json_file' not in request.files:
        return "No file part"
    
    file = request.files['json_file']
    
    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.endswith('.json'):
        file.save(os.path.join('uploads', file.filename))
        
        global stored_vectors
        with open(os.path.join('uploads', file.filename), 'r') as f:
            stored_vectors = json.load(f)
        
        return "JSON file uploaded and processed successfully."


@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/verify', methods=['POST'])
def verify():
    user_id = request.form['userID']
    user_password = request.form['userPassword']
    return redirect(url_for('purge_page'))

@app.route('/face_scan')
def face_scan():
    return render_template('face_scan.html')

@app.route('/report_status')
def report_status():
    return render_template('report_status.html')

@app.route('/report_history')
def report_history():
    return render_template('report_history.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image_file' not in request.files:
        return "No file part"
    
    file = request.files['image_file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        image = Image.open(file)
        image = np.array(image)
        faces = detector.detect_faces(image)
        
        if not faces:
            return "No face detected in the image."

        x, y, width, height = faces[0]['box']
        face_image = image[y:y+height, x:x+width]
        face_image = Image.fromarray(face_image).resize((160, 160))
        face_image = np.array(face_image)

        face_vector = embedder.embeddings([face_image])[0]
        best_match_url = None
        highest_similarity = -1
        
        for filename, vector in stored_vectors.items():
            stored_vector = np.array(vector)
            similarity = np.dot(face_vector, stored_vector) / (np.linalg.norm(face_vector) * np.linalg.norm(stored_vector))
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match_url = filename
        
        if highest_similarity > 0.6:
            print(f"Match: {best_match_url}, Similarity: {highest_similarity}")
            return redirect(url_for('purge_page', match=best_match_url, similarity=highest_similarity))
        else:
            print("No suitable match found.")
            return redirect(url_for('purge_page', match=None, similarity=highest_similarity))
    return "Invalid file format"

@app.route('/purge_page')
def purge_page():
    match = request.args.get('match')
    similarity = request.args.get('similarity')
    print(f"Received request for purge_page with match: {match}, similarity: {similarity}")

    if match:
        match = unquote(match)

    thumbnail_url = None
    if match:
        video_id = match.split('v=')[-1]
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    print(f"Decoded match: {match}, Similarity: {similarity}")
    return render_template('purge_page.html', match=match, similarity=similarity, thumbnail_url=thumbnail_url)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)