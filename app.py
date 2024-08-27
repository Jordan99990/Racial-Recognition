from fastai.vision.all import *
from flask import Flask, send_from_directory, request, jsonify
from PIL import Image
from facenet_pytorch import MTCNN
import io
import base64

app = Flask(__name__, static_folder='frontend/dist')

models = {
    'fastai v1': load_learner('./models/fairface_v1.pkl'),
    'fastai v2': load_learner('./models/fairface_v2.pkl'),
    'fastai v3': load_learner('./models/fairface_v3.pkl')
}

age_labels = ['0-2', '3-9', '10-19', '20-29', '30-39', 
              '40-49', '50-59', '60-69', 'more than 70']
race_labels = ['White', 'Black', 'East Asian', 'Southeast Asian',
               'Indian', 'Middle Eastern', 'Latino_Hispanic']
gender_labels = ['Male', 'Female']

@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def assets(path):
    return send_from_directory(app.static_folder, path)

@app.route('/predict', methods=['POST'])
def predict():
    def detect_face_mtcnn(img):
        mtcnn = MTCNN(
            image_size=224,
            margin=20,
            keep_all=True,
            post_process=True,
            select_largest=False,
            thresholds=[0.6, 0.7, 0.7]  
        )
        
        faces, _ = mtcnn.detect(img)
            
        if faces is None:
            return img
            
        for (x1, y1, x2, y2) in faces:
            face = img.crop((x1, y1, x2, y2))
            return face
        return img
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img = Image.open(file).convert('RGB')

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        original_img_str = base64.b64encode(buffered.getvalue()).decode()

        face_img = detect_face_mtcnn(img)

        buffered = io.BytesIO()
        face_img.save(buffered, format="JPEG")
        detected_face_img_str = base64.b64encode(buffered.getvalue()).decode()

        all_predictions = {}

        for model_name, model in models.items():
            pred, pred_idx, probs = model.predict(face_img)
            
            ethnicity_probs = {race_labels[i]: round(probs[i].item() * 100, 1) for i in range(len(race_labels))}
            age_pred = {age_labels[i]: round(probs[i + len(race_labels)].item() * 100, 1) for i in range(len(age_labels))}
            gender_pred = {gender_labels[i]: round(probs[i + len(race_labels) + len(age_labels)].item() * 100, 1) for i in range(len(gender_labels))}
            
            all_predictions[model_name] = {
                'ethnicity': ethnicity_probs,
                'age': age_pred,
                'gender': gender_pred,
                'originalImage': original_img_str,
                'detectedFaceImage': detected_face_img_str
            }

        print(all_predictions)
        return jsonify(all_predictions)
        
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)