from flask import Flask, send_from_directory, request, jsonify
from fastai.vision.all import load_learner, PILImage
from typing import Dict
import torch

app = Flask(__name__, static_folder='frontend/dist')
learn = load_learner('./models/fastai_model_v2.pkl')

if torch.cuda.is_available():
    learn.model.cuda()

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
        img = PILImage.create(file)

        pred, pred_idx, probs = learn.predict(img)
        probabilities = {ethnicity_labels[i]: p.item() for i, p in enumerate(probs)}
        
        print(probabilities)
        return jsonify(probabilities)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)