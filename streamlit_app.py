import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="Potato Disease Detection",
    page_icon="🥔",
    layout="wide"
)

# Load model dan labels
@st.cache_resource
def load_model_and_labels():
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
    
    return interpreter, input_details, output_details, labels

def preprocess_image(image, input_details):
    """
    Preprocess image untuk model TensorFlow Lite
    """
    try:
        # Convert ke RGB jika perlu
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize sesuai input model
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
        st.error(f"Error preprocessing image: {str(e)}")
        return None

def predict_disease(image_array, interpreter, input_details, output_details):
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
        st.error(f"Error during prediction: {str(e)}")
        return None, None, None

# Main app
def main():
    st.title("🥔 Potato Disease Detection")
    st.write("Upload gambar daun kentang untuk mendeteksi penyakit")
    
    # Load model
    try:
        interpreter, input_details, output_details, labels = load_model_and_labels()
        st.success("✅ Model berhasil dimuat!")
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Pilih gambar daun kentang",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
        help="Format yang didukung: PNG, JPG, JPEG, GIF, BMP, WEBP"
    )
    
    if uploaded_file is not None:
        # Display image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Gambar Input")
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar yang diupload", use_column_width=True)
        
        with col2:
            st.subheader("🔍 Hasil Deteksi")
            
            # Preprocess image
            with st.spinner("Memproses gambar..."):
                image_array = preprocess_image(image, input_details)
            
            if image_array is not None:
                # Predict
                with st.spinner("Mendeteksi penyakit..."):
                    predicted_class, confidence, all_predictions = predict_disease(
                        image_array, interpreter, input_details, output_details
                    )
                
                if predicted_class is not None:
                    # Set threshold
                    threshold = 0.5
                    
                    if confidence < threshold:
                        st.warning("⚠️ **Penyakit tidak terdeteksi**")
                        st.write(f"Confidence: {confidence * 100:.2f}%")
                    else:
                        label = labels[predicted_class]
                        percentage = f"{confidence * 100:.2f}%"
                        
                        st.success(f"✅ **Penyakit terdeteksi: {label}**")
                        st.write(f"**Confidence:** {percentage}")
                        
                        # Progress bar untuk confidence
                        st.progress(confidence)
                        
                        # Top 3 predictions
                        st.subheader("📊 Top 3 Prediksi")
                        top_3_indices = np.argsort(all_predictions)[-3:][::-1]
                        
                        for i, idx in enumerate(top_3_indices):
                            conf = all_predictions[idx] * 100
                            st.write(f"{i+1}. **{labels[idx]}**: {conf:.2f}%")
                            st.progress(all_predictions[idx])
    
    # Sidebar info
    with st.sidebar:
        st.header("ℹ️ Informasi")
        st.write("**Penyakit yang dapat dideteksi:**")
        try:
            interpreter, input_details, output_details, labels = load_model_and_labels()
            for i, label in enumerate(labels):
                st.write(f"{i+1}. {label}")
        except:
            st.write("Model belum dimuat")
        
        st.write("---")
        st.write("**Cara Penggunaan:**")
        st.write("1. Upload gambar daun kentang")
        st.write("2. Tunggu proses deteksi")
        st.write("3. Lihat hasil prediksi")
        
        st.write("---")
        st.write("**Format yang didukung:**")
        st.write("PNG, JPG, JPEG, GIF, BMP, WEBP")

if __name__ == "__main__":
    main()
