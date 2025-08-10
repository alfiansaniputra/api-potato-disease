# Potato Disease Detection API

API untuk deteksi penyakit kentang menggunakan TensorFlow Lite model.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
python app.py
```

API akan berjalan di `http://localhost:3000`

## Endpoints

### 1. `/detect` (GET)
Endpoint utama untuk deteksi penyakit kentang.

**Method:** GET  
**Content-Type:** multipart/form-data  
**Parameter:** 
- `file` (required): File gambar (png, jpg, jpeg, gif, bmp, webp)

**Response Success:**
```json
{
  "detected": true,
  "label": "Bercak Kering",
  "percentage": "85.23%",
  "confidence": 0.8523,
  "top_predictions": [
    {
      "label": "Bercak Kering",
      "confidence": "85.23%"
    },
    {
      "label": "Layu",
      "confidence": "10.45%"
    },
    {
      "label": "Busuk daun",
      "confidence": "4.32%"
    }
  ]
}
```

**Response Not Detected:**
```json
{
  "detected": false,
  "message": "Penyakit tidak terdeteksi",
  "confidence": "35.67%"
}
```

**Response Error:**
```json
{
  "error": "Error type",
  "message": "Error description"
}
```

### 2. `/health` (GET)
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Potato disease detection API is running",
  "model_loaded": true,
  "labels_loaded": true
}
```

### 3. `/` (GET)
API information dan dokumentasi.

## Penyakit yang Dapat Dideteksi

1. Bercak Kering
2. Busuk daun
3. Cincin bakteri
4. Daun menggulung
5. Fusarium
6. Kutu daun
7. Lalat
8. Layu
9. Mozaik
10. Nematoda
11. Penggerek daun

## Contoh Penggunaan

### Using cURL:
```bash
curl -X GET \
  -F "file=@path/to/your/image.jpg" \
  http://localhost:3000/detect
```

### Using Python requests:
```python
import requests

url = "http://localhost:3000/detect"
files = {"file": open("path/to/your/image.jpg", "rb")}
response = requests.get(url, files=files)
print(response.json())
```

### Using Postman:
1. Set method to GET
2. Go to Body tab
3. Select form-data
4. Add key "file" with type "File"
5. Upload your image file
6. Send request to `http://localhost:3000/detect`

## Deployment

Untuk production, gunakan gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

## Model Information

- **Model:** TensorFlow Lite (model_unquant.tflite)
- **Input Size:** Auto-detected dari model
- **Normalization:** [0, 1]
- **Threshold:** 0.5 (50% confidence untuk deteksi positif)
