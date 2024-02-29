import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
import json
import numpy as np 

# Load your model
model = tf.keras.models.load_model('chest_xray_model.h5')  
image_size = (224, 224)

disease_labels = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 
                'Edema', 'Emphysema', 'Fibrosis', 'Effusion', 'Pneumonia', 
                'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', 'Hernia', 'No Finding']

def predict_disease(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_png(img, channels=3)
    img = tf.image.resize(img, image_size)
    img = preprocess_input(img)  # Use VGG16 preprocessing
    prediction = model.predict(tf.expand_dims(img, axis=0))[0] 

    # Create results dictionary
    results = {
        'predictions': [label for label, prob in zip(disease_labels, prediction) if prob > 0.5],
        'confidence': prediction.tolist()  
    }

    return json.dumps(results)  # Return as JSON string

# Let's assume you get the image_path from command-line arguments
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = predict_disease(image_path)
        print(result) 
    else:
        print("Please provide the image path.")