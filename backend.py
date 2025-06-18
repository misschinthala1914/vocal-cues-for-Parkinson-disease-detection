from flask import Flask, request, jsonify
import numpy as np
import librosa
import soundfile as sf
import io
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import tensorflow as tf
from datetime import datetime

app = Flask(__name__)

# Load pre-trained models (in a real app, these would be properly trained models)
xgboost_model = xgb.XGBClassifier()  # This would be loaded from a file
densenet_model = tf.keras.models.load_model('densenet_model.h5')  # Example
scaler = StandardScaler()  # This would be fitted with training data

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    try:
        # Get audio file from request
        audio_file = request.files['audio']
        file_content = audio_file.read()
        
        # Convert to numpy array
        audio, sr = librosa.load(io.BytesIO(file_content), sr=None)
        
        # Extract features (simplified - real implementation would extract more features)
        features = extract_vocal_features(audio, sr)
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Get predictions
        xgboost_pred = xgboost_model.predict_proba(features_scaled)[0][1]
        densenet_pred = densenet_model.predict(features_scaled.reshape(1, -1, 1))[0][0]
        
        # Ensemble prediction (weighted average)
        our_pred = (xgboost_pred * 0.4 + densenet_pred * 0.6)
        
        # Determine final prediction
        final_prediction = 'positive' if our_pred > 0.5 else 'negative'
        
        # Prepare response
        response = {
            'timestamp': datetime.now().isoformat(),
            'prediction': final_prediction,
            'confidence': {
                'xgboost': round(float(xgboost_pred * 100), 2),
                'densenet': round(float(densenet_pred * 100), 2),
                'ourModel': round(float(our_pred * 100), 2)
            },
            'features': {
                'jitter': round(features[0], 4),
                'shimmer': round(features[1], 4),
                'hnr': round(features[2], 2),
                'pitchVariation': round(features[3], 4),
                # Add more features as needed
            },
            'message': 'Analysis complete'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_vocal_features(audio, sr):
    """Extract vocal features from audio signal"""
    # In a real implementation, this would extract many more features
    # These are placeholder calculations
    
    # Jitter (simulated)
    jitter = np.random.uniform(0.001, 0.02)
    
    # Shimmer (simulated)
    shimmer = np.random.uniform(0.01, 0.1)
    
    # Harmonic-to-noise ratio (simulated)
    hnr = np.random.uniform(5, 20)
    
    # Pitch variation (simulated)
    pitch_variation = np.random.uniform(0.1, 0.5)
    
    # Return as array (in real app, would return many more features)
    return np.array([jitter, shimmer, hnr, pitch_variation])

if __name__ == '__main__':
    app.run(debug=True)