import tensorflow as tf
from tensorflow.keras.models import load_model
import json
import numpy as np 

# Load your model
model = tf.keras.models.load_model('chest_xray_model.h5')  
image_size = (224, 224)

# NEEDS TO BE FIXED BELOW -- 
disease_labels = ['Atelectasis', 'Consolidation', ..., 'Hernia'] # 14 diseases

def predict_disease(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_png(img, channels=3)
    img = tf.image.resize(img, image_size)
    img = tf.keras.applications.vgg16.preprocess_input(img)  # VGG16 specific   
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