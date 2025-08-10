from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

# Load model dan labels saat aplikasi dimulai
model_path = os.path.join(os.path.dirname(__file__), 'model', 'model_unquant.tflite')
labels_path = os.path.join(os.path.dirname(__file__), 'model', 'labels.txt')

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load labels
with open(labels_path, 'r') as f:
    labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]

def preprocess_image(image_file):
    """
    Preprocess image untuk model TensorFlow Lite
    """
    try:
        # Buka image dari file
        image = Image.open(io.BytesIO(image_file.read()))
        
        # Convert ke RGB jika perlu
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize sesuai input model (biasanya 224x224 untuk model klasifikasi)
        input_shape = input_details[0]['shape']
        height, width = input_shape[1], input_shape[2]
        image = image.resize((width, height))
        
        # Convert ke numpy array dan normalize
        image_array = np.array(image, dtype=np.float32)
        image_array = image_array / 255.0  # Normalize ke range [0, 1]
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")

def predict_disease(image_array):
    """
    Prediksi penyakit menggunakan model TensorFlow Lite
    """
    try:
        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], image_array)
        
        # Run inference
        interpreter.invoke()
        
        # Get output
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predictions = output_data[0]
        
        # Get predicted class dan confidence
        predicted_class = np.argmax(predictions)
        confidence = float(predictions[predicted_class])
        
        return predicted_class, confidence, predictions
    except Exception as e:
        raise ValueError(f"Error during prediction: {str(e)}")

@app.route('/detect', methods=['POST'])  # Changed to POST for file upload
def detect_disease():
    """
    API endpoint untuk deteksi penyakit kentang
    Input: file gambar melalui form-data dengan key 'file'
    Output: JSON dengan label dan persentase confidence
    """
    try:
        # Check apakah ada file dalam request
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'message': 'Please upload an image file with key "file"'
            }), 400
        
        file = request.files['file']
        
        # Check apakah file kosong
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select a file to upload'
            }), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            return jsonify({
                'error': 'Invalid file type',
                'message': f'Allowed file types: {", ".join(allowed_extensions)}'
            }), 400
        
        # Preprocess image
        try:
            image_array = preprocess_image(file)
        except ValueError as e:
            return jsonify({
                'error': 'Image preprocessing failed',
                'message': str(e)
            }), 400
        
        # Predict
        try:
            predicted_class, confidence, all_predictions = predict_disease(image_array)
        except ValueError as e:
            return jsonify({
                'error': 'Prediction failed',
                'message': str(e)
            }), 500
        
        # Set threshold untuk deteksi (misalnya 0.5 atau 50%)
        threshold = 0.5
        
        if confidence < threshold:
            return jsonify({
                'detected': False,
                'message': 'Penyakit tidak terdeteksi',
                'confidence': f"{confidence * 100:.2f}%"
            })
        
        # Return hasil prediksi
        label = labels[predicted_class]
        percentage = f"{confidence * 100:.2f}%"
        
        # Get top 3 predictions untuk informasi tambahan
        top_3_indices = np.argsort(all_predictions)[-3:][::-1]
        top_3_predictions = []
        
        for idx in top_3_indices:
            top_3_predictions.append({
                'label': labels[idx],
                'confidence': f"{all_predictions[idx] * 100:.2f}%"
            })
        
        return jsonify({
            'detected': True,
            'label': label,
            'percentage': percentage,
            'confidence': confidence,
            'top_predictions': top_3_predictions
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Potato disease detection API is running',
        'model_loaded': os.path.exists(model_path),
        'labels_loaded': os.path.exists(labels_path)
    })

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint dengan informasi API
    """
    return jsonify({
        'message': 'Potato Disease Detection API',
        'version': '1.0.0',
        'endpoints': {
            '/detect': 'POST - Upload image for disease detection',
            '/health': 'GET - Health check',
            '/': 'GET - API information'
        },
        'usage': {
            'endpoint': '/detect',
            'method': 'POST',
            'content_type': 'multipart/form-data',
            'file_key': 'file',
            'supported_formats': ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']
        }
    })

# Removed the if __name__ == '__main__' block for deployment
# This allows the app to be imported by WSGI servers like Gunicorn
