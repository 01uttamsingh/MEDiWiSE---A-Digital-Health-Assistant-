import os
import threading
import joblib
import pandas as pd
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class SymptomPredictorService:
    """
    Singleton service that loads Random Forest symptom prediction models
    and provides disease prediction and precaution mapping.
    """
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.model = None
        self.symptom_encoder = None
        self.label_encoder = None
        self.precaution_df = None
        self._is_loaded = False
        self._load_models()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _load_models(self):
        try:
            model_path = os.path.join(settings.MODELS_DIR, 'symptom_disease_model_rf.pkl')
            symptom_enc_path = os.path.join(settings.MODELS_DIR, 'symptom_encoder.pkl')
            label_enc_path = os.path.join(settings.MODELS_DIR, 'label_encoder.pkl')
            precaution_path = os.path.join(settings.DATASETS_DIR, 'Disease precaution.csv')

            logger.info("Loading symptom prediction models and dataset...")
            self.model = joblib.load(model_path)
            self.symptom_encoder = joblib.load(symptom_enc_path)
            self.label_encoder = joblib.load(label_enc_path)
            self.precaution_df = pd.read_csv(precaution_path)
            self._is_loaded = True
            logger.info("Symptom prediction service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to load symptom models or data: {e}", exc_info=True)
            self._is_loaded = False

    @property
    def is_ready(self):
        return self._is_loaded and self.model is not None

    def predict(self, symptoms_list):
        """
        Predict disease from a list of symptom strings.
        Returns:
            dict with 'disease', 'accuracy', and 'precautions' keys,
            or dict with 'error' key.
        """
        if not self.is_ready:
            return {"error": "Server-side models or data are not loaded.", "status_code": 500}

        if not symptoms_list or not isinstance(symptoms_list, list):
            return {"error": "Please provide a non-empty list of symptoms.", "status_code": 400}

        # Normalize symptom names to match training format
        processed_symptoms = [s.strip().lower().replace(" ", "_") for s in symptoms_list if isinstance(s, str)]
        valid_symptoms = [s for s in processed_symptoms if s in self.symptom_encoder.classes_]

        if not valid_symptoms:
            return {
                "error": "No valid symptoms provided or symptoms are not recognized by the model.",
                "status_code": 400
            }

        try:
            # Build one-hot input vector matching feature names
            input_vector = pd.DataFrame(0, index=[0], columns=self.symptom_encoder.classes_)
            for symptom in valid_symptoms:
                input_vector[symptom] = 1

            predicted_disease_index = self.model.predict(input_vector)[0]
            confidence = max(self.model.predict_proba(input_vector)[0]) * 100
            predicted_disease_name = self.label_encoder.inverse_transform([predicted_disease_index])[0]

            # Precautions lookup
            precautions_row = self.precaution_df[self.precaution_df['Disease'] == predicted_disease_name]
            if not precautions_row.empty:
                precautions = precautions_row.iloc[0, 1:].dropna().tolist()
            else:
                precautions = ["No specific precautions found."]

            return {
                "disease": str(predicted_disease_name),
                "accuracy": f"{confidence:.2f}%",
                "precautions": precautions,
                "status_code": 200
            }
        except Exception as e:
            logger.error(f"Error during symptom prediction inference: {e}", exc_info=True)
            return {"error": "An internal server error occurred during prediction.", "status_code": 500}
