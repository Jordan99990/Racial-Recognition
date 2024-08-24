from fastai.vision.all import *
from flask import Flask, send_from_directory, request, jsonify
import torch
from PIL import Image

app = Flask(__name__, static_folder='frontend/dist')

models = {
    # 'fastai v1': load_learner('./models/fairface_v1.pkl'),
    'fastai v2': load_learner('./models/fairface_v2.pkl'),
    'fastai v3': load_learner('./models/fairface_v3.pkl')
}

ethnicity_labels = [
    'White', 'Black', 'East Asian', 'Southeast Asian', 
    'Indian', 'Middle Eastern', 'Latino_Hispanic'
]

@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def assets(path):
    return send_from_directory(app.static_folder, path)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img = Image.open(file).convert('RGB')
        all_predictions = {}

        for model_name, model in models.items():
            pred, pred_idx, probs = model.predict(img)
            ethnicity_probs = {ethnicity_labels[i]: round(probs[i].item() * 100, 1) for i in range(len(ethnicity_labels))}
            all_predictions[model_name] = ethnicity_probs

        print(all_predictions)
        return jsonify(all_predictions)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)