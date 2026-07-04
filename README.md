# MEDiWiSE — A Digital Health Assistant

An AI-powered web application that helps users predict diseases from symptoms, detect skin diseases from images, and get home remedies — all in one place.

---

## Features

- **Symptom-based Disease Prediction** — ML model (Random Forest) predicts disease from entered symptoms with confidence score
- **Skin Disease Detection** — Deep learning model (EfficientNet-B0) classifies 7 skin conditions from uploaded images
- **Home Remedies Chatbot** — Gemini AI suggests home remedies for any disease
- **General Health Chatbot (MedTed)** — AI health assistant for general health queries
- **Nearby Hospitals & Pharmacies** — Google Maps integration to find medical help nearby
- **Emergency Call** — One-tap call to emergency number 108

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML Model | Scikit-learn (Random Forest) |
| DL Model | PyTorch, EfficientNet-B0 |
| AI Chatbot | Google Gemini API (`gemini-2.5-flash`) |
| Maps | Google Maps JavaScript API |
| Frontend | HTML, CSS (Jinja2 templates) |

---

## Project Structure

```
UI-MEDiWiSE(final)/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # API keys (NOT committed — see .env.sample)
├── .env.sample             # Template for environment variables
├── templates/              # HTML pages (Jinja2)
├── static/                 # CSS, images, icons
├── models/                 # Trained ML/DL model files (.pkl, .pth)
├── datasets/               # Disease precaution CSV data
├── chatbots/               # Standalone chatbot scripts
└── utils/                  # Utility wrappers
```

---

## Setup Guide

### Prerequisites

- Python 3.9 or higher
- pip
- A Google Gemini API key → [Get one here](https://aistudio.google.com/app/apikey)
- A Google Maps API key → [Get one here](https://console.cloud.google.com/apis/credentials)

---

### 1. Clone the Repository

```bash
git clone https://github.com/01uttamsingh/MEDiWiSE---A-Digital-Health-Assistant-.git
cd MEDiWiSE---A-Digital-Health-Assistant-
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the sample file and fill in your API keys:

```bash
# Windows
copy .env.sample .env

# macOS/Linux
cp .env.sample .env
```

Open `.env` and replace the placeholder values:

```
GEMINI_API_KEY=your_actual_gemini_api_key
GOOGLE_MAPS_API_KEY=your_actual_google_maps_api_key
```

### 5. Run the Application

```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

---

## API Keys Required

| Key | Purpose | Where to Get |
|---|---|---|
| `GEMINI_API_KEY` | Powers all AI chatbot features | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `GOOGLE_MAPS_API_KEY` | Nearby hospitals/pharmacies map on Help page | [Google Cloud Console](https://console.cloud.google.com/apis/credentials) |

> Enable **Maps JavaScript API** and **Places API** in your Google Cloud project for the map features to work.

---

## Models Included

| File | Description |
|---|---|
| `models/symptom_disease_model_rf.pkl` | Random Forest model for symptom prediction |
| `models/symptom_encoder.pkl` | MultiLabelBinarizer for symptom encoding |
| `models/label_encoder.pkl` | Label encoder for disease names |
| `models/skin_model.pth` | EfficientNet-B0 weights for skin disease detection |

---

## Skin Disease Classes

The DL model detects 7 conditions:

| Code | Disease |
|---|---|
| AD | Atopic Dermatitis |
| CD | Contact Dermatitis |
| EC | Eczema |
| SC | Scabies |
| SD | Seborrheic Dermatitis |
| TC | Tinea Corporis |
| OOD | Out-of-distribution (no disease) |

---

## Disclaimer

> MEDiWiSE is an AI-assisted tool for general health guidance only. It is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare provider for medical concerns.

---



---

## License

This project is for educational purposes.
