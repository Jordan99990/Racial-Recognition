from fastai.vision.all import *
from flask import Flask, send_from_directory, request, jsonify
import torch
from PIL import Image

app = Flask(__name__, static_folder='frontend/dist')
model1 = load_learner('./models/fastai_model_v3.pkl')

@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def assets(path):
    return send_from_directory(app.static_folder, path)

@app.route('/predict', methods=['POST'])
def predict():
    ethnicity_labels = {
        0: 'White',
        1: 'Black',
        2: 'Asian',
        3: 'Indian',
        4: 'Others'
    }
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img = Image.open(file).convert('RGB')

        pred, pred_idx, probs = model1.predict(img)
        
        probabilities = {ethnicity_labels[i]: round(p.item() * 100, 1) for i, p in enumerate(probs)}
        
        print(probabilities)
        return jsonify(probabilities)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)