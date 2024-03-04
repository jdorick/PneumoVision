from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for hosting
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://127.0.0.1:3000"}})

# Load your model
model = tf.keras.models.load_model(r'C:\Users\jdori\Downloads\chest_xray_model_vgg16.h5')
image_size = (224, 224)

disease_labels = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax',
                  'Edema', 'Emphysema', 'Fibrosis', 'Effusion', 'Pneumonia',
                  'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', 'Hernia', 'No Finding']

def preprocess_image(image):
    img = tf.image.resize(image, image_size)
    img = preprocess_input(img)
    return img

def predict_disease(image):
    image = preprocess_image(image)
    prediction = model.predict(tf.expand_dims(image, axis=0))[0]

    results = {
        'predictions': [label for label, prob in zip(disease_labels, prediction) if prob > 0.5],
        'confidence': prediction.tolist()
    }

    return results

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image'].read()
    image = tf.image.decode_image(image, channels=3)
    
    result = predict_disease(image)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)