from flask import Flask, request, jsonify
from prediction import predict_disease

app = Flask(__name__)

# Endpoint for image prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Assuming the image is sent as a file in the 'image' field of the form data
        uploaded_file = request.files['image']
        if uploaded_file.filename != '':
            result = predict_disease(uploaded_file)
            return jsonify(result)
        else:
            return jsonify({'error': 'No file provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)