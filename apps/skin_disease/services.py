import os
import io
import threading
import logging
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
from django.conf import settings

logger = logging.getLogger(__name__)

class SkinDiseasePredictionService:
    """
    Singleton service managing the PyTorch EfficientNet-B0 skin disease classifier.
    Handles image preprocessing, batch transformation, model inference,
    and class mapping.
    """
    _instance = None
    _lock = threading.Lock()

    SKIN_CLASS_NAMES = ['AD', 'CD', 'EC', 'OOD', 'SC', 'SD', 'TC']

    DISEASE_MAP = {
        "AD": "Atopic Dermatitis",
        "CD": "Contact Dermatitis",
        "EC": "Eczema",
        "SC": "Scabies",
        "SD": "Seborrheic Dermatitis",
        "TC": "Tinea Corporis",
        "OOD": "No disease predicted! (Check again, photo may be inappropriate)"
    }

    PRECAUTIONS_MAP = {
        "AD": ["Consult a dermatologist and keep the area clean."],
        "CD": ["Avoid irritants and apply soothing creams."],
        "EC": ["Keep skin moisturized and avoid scratching."],
        "SC": ["Use medicated cream and wash clothes properly."],
        "SD": ["Apply antifungal creams and keep skin dry."],
        "TC": ["Consult a doctor and follow treatment instructions."]
    }

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.transforms = None
        self._is_loaded = False
        self._initialize_service()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _initialize_service(self):
        try:
            model_path = os.path.join(settings.MODELS_DIR, 'skin_model.pth')
            logger.info(f"Loading skin disease EfficientNet model from {model_path} onto {self.device}...")

            model = models.efficientnet_b0(weights=None)
            model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(self.SKIN_CLASS_NAMES))
            model.load_state_dict(torch.load(model_path, map_location=self.device))
            model.to(self.device)
            model.eval()

            self.model = model

            self.transforms = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

            self._is_loaded = True
            logger.info("Skin disease prediction service initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing skin disease model: {e}", exc_info=True)
            self._is_loaded = False

    @property
    def is_ready(self):
        return self._is_loaded and self.model is not None

    def predict(self, image_bytes):
        """
        Run inference on image bytes and return predicted skin condition details.
        """
        if not self.is_ready:
            return {"error": "Skin model is not loaded on the server.", "status_code": 500}

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            image_tensor = self.transforms(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, pred_idx = torch.max(probabilities, 1)

            predicted_class_abbr = self.SKIN_CLASS_NAMES[pred_idx.item()]
            confidence_score = f"{confidence.item() * 100:.2f}%"
            disease_name = self.DISEASE_MAP.get(predicted_class_abbr, "Unknown Prediction")

            if predicted_class_abbr == "OOD":
                precautions = "Nothing to be display"
            else:
                precautions = self.PRECAUTIONS_MAP.get(
                    predicted_class_abbr,
                    ["No specific precautions found."]
                )

            return {
                "disease": disease_name,
                "confidence": confidence_score,
                "precautions": precautions,
                "status_code": 200
            }

        except Exception as e:
            logger.error(f"Error during skin disease image prediction: {e}", exc_info=True)
            return {"error": "An error occurred while processing the image.", "status_code": 500}
