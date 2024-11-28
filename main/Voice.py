#!/usr/bin/env python
# coding: utf-8

# In[102]:


# Load the saved model and scaler
with open('parkinsons_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Load the saved imputer (to handle missing values in the features)
with open('imputer.pkl', 'rb') as imputer_file:
    imputer = pickle.load(imputer_file)


# In[103]:


import pyaudio
import wave

def record_audio(filename='user_audio.wav', duration=5, sample_rate=16000):
    """Record audio from the microphone and save it as a .wav file."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    
    print("Recording...")
    print("Please Read the Following Paragrapgh...")
    print('''The quick brown fox jumps over the lazy dog near a quiet riverbank.
     As the sun sets, the calm breeze rustles the leaves, creating a soothing sound.
     In the distance, a clock tower chimes, marking the end of another day. Every moment counts,
     and every word we speak carries a meaning, shaping the world around us. 
     Speak clearly, and let your voice express the thoughts within your mind.''')
    frames = []
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

record_audio()


# In[104]:


import librosa
import numpy as np

def extract_features(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Extract MFCC (13 coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_scaled = np.mean(mfcc.T, axis=0)

    # Extract additional features
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85))
    chroma_mean = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))

    # Combine features
    features = np.hstack((mfcc_scaled, zcr, rolloff, chroma_mean))  # Shape: (16,)

    # Pad to 22 features if needed
    if len(features) < 22:
        features = np.pad(features, (0, 22 - len(features)), 'constant')

    return features


# In[ ]:


# print(f"Scaler expected input shape: {scaler.n_features_in_}")


# In[ ]:





# In[ ]:


def predict_parkinsons(audio_file):
    """Predict Parkinson's disease from an audio file."""
    print("Starting feature extraction...")
    features = extract_features(audio_file)
    print(f"Extracted features: {features}")

    # Check feature length
    if len(features) != scaler.n_features_in_:
        raise ValueError(f"Feature shape mismatch: expected {scaler.n_features_in_} features, got {len(features)}")
    
    print("Scaling features...")
    features_scaled = scaler.transform([features])
    print(f"Scaled features: {features_scaled}")

    print("Making prediction...")
    prediction = model.predict(features_scaled)
    prediction_proba = model.predict_proba(features_scaled)
    # print(f"Prediction: {prediction}")
    print(f"Prediction probabilities: {prediction_proba[0]}")

    # Print final result
    if prediction_proba[0][0]>0.7:
        print(f"Prediction: Parkinson's disease detected with probability {prediction_proba[0][1]:.2f}")
    else:
        print(f"Prediction: No Parkinson's disease detected with probability {prediction_proba[0][0]:.2f}")


# In[107]:


try:
    predict_parkinsons('user_audio.wav')
except Exception as e:
    print(f"Error: {e}")


# In[ ]:





# In[ ]:




