from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for handling Cross-Origin Resource Sharing (CORS)
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})  # Allow CORS for the /predict route

# Load the model
model = tf.keras.models.load_model(r'C:\\Users\\jdorick\\Downloads\\chest_xray_model_resnet.h5')

# Load your model
model = tf.keras.models.load_model(r'C:\Users\jdori\Downloads\chest_xray_model_vgg16.h5')
image_size = (224, 224)
# All disease labels
disease_labels = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax',
                  'Edema', 'Emphysema', 'Fibrosis', 'Effusion', 'Pneumonia',
                  'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', 'Hernia', 'No Finding'] 

def preprocess_image(image):
    img = tf.image.resize(image, image_size)
    img = preprocess_input(img)
    return img

def predict_disease(image):
    image = preprocess_image(image)
    prediction = model.predict(tf.expand_dims(image, axis=0))[0]  # Get the prediction scores
    max_index = np.argmax(prediction)  # Find the index of the maximum confidence
    results = {
        'prediction': disease_labels[max_index],  # Predicted disease label
        'confidence': float(prediction[max_index])  # Prediction confidence score
    }
    return results

@app.route('/predict', methods=['POST'])
def predict():
    print('Received POST request')
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400  # Return an error if no image is provided

    # Read the image data from the request
    image = request.files['image'].read()
    image = tf.image.decode_image(image, channels=3)  # Decode the image data

    result = predict_disease(image)  # Get the prediction result
    return jsonify(result)  # Return the prediction result as JSON

if __name__ == '__main__':
    app.run(debug=True, port=5000)