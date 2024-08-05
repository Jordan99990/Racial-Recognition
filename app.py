from flask import Flask, send_from_directory, request, jsonify
from fastai.vision.all import load_learner, PILImage
import io

app = Flask(__name__, static_folder='frontend/dist')
model = load_learner('./models/fastai_model_v1.pkl')

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
        img = PILImage.create(io.BytesIO(file.read()))
        pred, pred_idx, probs = model.predict(img)
        result = {
            model.dls.vocab[i]: p.item() for i, p in enumerate(probs)
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)