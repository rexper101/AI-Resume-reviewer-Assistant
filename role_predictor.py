"""
role_predictor.py - ML classification model for predicting suitable job roles.
Trains on synthetic resume data using TF-IDF + Logistic Regression.
"""

import numpy as np
import logging
import warnings
warnings.filterwarnings('ignore')

from typing import Dict, List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

import sys
sys.path.insert(0, os.path.dirname(__file__))
from datasets.job_descriptions import JOB_ROLES
import config

logger = logging.getLogger(__name__)

# ── Model configuration constants ──────────────────────────────────────────────
VALID_MODEL_TYPES = {"logistic_regression", "random_forest", "naive_bayes"}
DEFAULT_MODEL_TYPE = "logistic_regression"
MIN_TRAINING_SAMPLES = 10
TEST_SIZE = 0.2
RANDOM_STATE = 42

# ── Synthetic training data ────────────────────────────────────────────────────
TRAINING_TEMPLATES = {
    "Data Scientist": [
        "python machine learning deep learning tensorflow scikit-learn pandas numpy statistics data visualization NLP AWS spark feature engineering",
        "data science machine learning python SQL statistics R tensorflow keras scikit-learn jupyter pandas data analysis predictive modeling",
        "python tensorflow pytorch deep learning neural networks NLP transformers BERT data preprocessing feature engineering model deployment AWS",
        "machine learning python statistics scikit-learn pandas numpy matplotlib seaborn plotly data visualization SQL postgres jupyter",
        "data scientist python R machine learning statistical analysis hypothesis testing A/B testing feature engineering random forest XGBoost",
    ],
    "Data Analyst": [
        "SQL Excel Tableau Power BI python pandas data analysis business intelligence reporting ETL data cleaning postgresql",
        "SQL data analysis Excel Tableau Power BI reporting business intelligence KPI metrics dashboards data visualization MySQL",
        "excel SQL Tableau data analysis business intelligence reporting stakeholder management data cleaning ETL data modeling",
        "python pandas SQL data analysis visualization matplotlib seaborn plotly Excel Power BI reporting business analysis",
        "SQL MySQL PostgreSQL data analysis reporting Excel Power BI Tableau looker business intelligence data warehouse ETL",
    ],
    "ML Engineer": [
        "python machine learning MLOps docker kubernetes AWS FastAPI model deployment scikit-learn tensorflow CI/CD REST API",
        "MLOps docker kubernetes AWS machine learning model serving FastAPI python TensorFlow PyTorch CI/CD GitHub Actions",
        "python tensorflow pytorch model deployment docker kubernetes AWS SageMaker mlflow feature engineering REST API",
        "machine learning engineering python docker kubernetes CI/CD model monitoring A/B testing FastAPI microservices AWS",
    ],
    "Python Developer": [
        "python django FastAPI Flask REST API SQL postgresql celery redis docker git CI/CD linux backend development",
        "python backend django REST API postgresql MySQL docker kubernetes AWS CI/CD git unit testing celery SQLAlchemy",
        "python FastAPI docker postgresql redis REST API authentication JWT testing CI/CD GitHub Actions git linux",
    ],
    "Backend Developer": [
        "java Spring Boot REST API microservices docker kubernetes MySQL AWS CI/CD git linux backend development",
        "node.js express REST API MongoDB SQL docker kubernetes AWS CI/CD microservices authentication JWT git",
        "backend development python java node.js SQL NoSQL docker microservices REST API cloud AWS Azure",
    ],
    "Frontend Developer": [
        "react javascript typescript HTML CSS tailwind redux REST API git jest responsive design node.js webpack",
        "react.js typescript javascript HTML5 CSS3 styled-components redux REST API git jest CI/CD next.js",
        "javascript react next.js typescript CSS HTML REST API git unit testing node.js webpack tailwind",
    ],
    "DevOps Engineer": [
        "docker kubernetes Jenkins GitHub Actions CI/CD AWS EC2 S3 IAM terraform ansible linux shell scripting",
        "cloud infrastructure AWS Azure GCP docker kubernetes terraform ansible Jenkins monitoring prometheus grafana",
        "DevOps automation docker kubernetes Jenkins GitHub Actions terraform ansible linux python CI/CD deployment",
    ],
}


class RolePredictor:
    """
    ML classification model for predicting job roles from resume text.
    Uses TF-IDF vectorization with multiple classifier options.
    Includes input validation and error handling.
    """

    def __init__(self, model_type: str = DEFAULT_MODEL_TYPE):
        """
        Initialize the role predictor.

        Args:
            model_type: "logistic_regression", "random_forest", or "naive_bayes"
            
        Raises:
            ValueError: If model_type is invalid
        """
        if model_type not in VALID_MODEL_TYPES:
            logger.error(f"Invalid model_type: {model_type}. Must be one of {VALID_MODEL_TYPES}")
            raise ValueError(f"model_type must be one of {VALID_MODEL_TYPES}")
        
        self.model_type = model_type
        logger.info(f"Initializing RolePredictor with model type: {model_type}")
        
        # Use config for TfidfVectorizer
        vectorizer_config = {
            "ngram_range": config.ROLE_PREDICTOR_CONFIG["tfidf_ngram"],
            "max_features": config.ROLE_PREDICTOR_CONFIG["tfidf_max_features"],
            "stop_words": "english",
            "min_df": 1
        }
        self.vectorizer = TfidfVectorizer(**vectorizer_config)
        self.label_encoder = LabelEncoder()
        self.model = self._create_model(model_type)
        self.is_trained = False
        self.training_accuracy = 0.0
        self.classes: List[str] = []

    def _create_model(self, model_type: str):
        """
        Create the specified ML model using config.
        
        Args:
            model_type: Model type to create
            
        Returns:
            Initialized model object
        """
        models = {
            "logistic_regression": LogisticRegression(
                **config.ROLE_PREDICTOR_CONFIG["logistic_regression"]
            ),
            "random_forest": RandomForestClassifier(
                **config.ROLE_PREDICTOR_CONFIG["random_forest"],
                n_jobs=-1
            ),
            "naive_bayes": MultinomialNB(
                **config.ROLE_PREDICTOR_CONFIG["naive_bayes"]
            )
        }
        selected_model = models.get(model_type, models[DEFAULT_MODEL_TYPE])
        logger.debug(f"Created model: {type(selected_model).__name__}")
        return selected_model

    def train(self) -> Dict[str, object]:
        """
        Train the role prediction model on synthetic training data.

        Returns:
            Dict with training results and model metrics
            
        Raises:
            ValueError: If training data is insufficient
        """
        try:
            logger.info(f"Starting model training with {self.model_type}")
            
            # Prepare training data from TRAINING_TEMPLATES
            texts: List[str] = []
            labels: List[str] = []

            for role, role_samples in TRAINING_TEMPLATES.items():
                if not role_samples:
                    logger.warning(f"No training samples for role: {role}")
                    continue
                texts.extend(role_samples)
                labels.extend([role] * len(role_samples))

            # Validate training data
            if len(texts) < MIN_TRAINING_SAMPLES:
                logger.error(f"Insufficient training samples: {len(texts)}")
                raise ValueError(f"Need at least {MIN_TRAINING_SAMPLES} training samples")

            logger.info(f"Training on {len(texts)} samples, {len(set(labels))} classes")

            # Encode labels
            self.label_encoder.fit(labels)
            encoded_labels = self.label_encoder.transform(labels)
            self.classes = list(self.label_encoder.classes_)

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                texts, encoded_labels, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=encoded_labels
            )

            # Vectorize
            logger.debug("Vectorizing training data with TF-IDF")
            X_train_vec = self.vectorizer.fit_transform(X_train)
            X_test_vec = self.vectorizer.transform(X_test)

            # For Naive Bayes, values must be non-negative (TF-IDF is already non-negative)
            # Train model
            logger.debug(f"Training {self.model_type} classifier")
            self.model.fit(X_train_vec, y_train)

            # Evaluate
            y_pred = self.model.predict(X_test_vec)
            accuracy = accuracy_score(y_test, y_pred)

            self.is_trained = True
            self.training_accuracy = accuracy
            
            logger.info(f"Model training complete. Accuracy: {accuracy * 100:.1f}%")

            return {
                "accuracy": round(accuracy * 100, 1),
                "model_type": self.model_type,
                "training_samples": len(X_train),
                "test_samples": len(X_test),
                "num_classes": len(self.classes),
                "classes": self.classes
            }
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise

    def predict(self, resume_text: str, skills: Optional[List[str]] = None) -> Dict[str, object]:
        """
        Predict the most suitable role for a resume.

        Args:
            resume_text: Full resume text
            skills: Optional extracted skills list (improves prediction)

        Returns:
            Dict with prediction result and probabilities
            
        Raises:
            ValueError: If resume_text is empty
        """
        if not resume_text or not resume_text.strip():
            logger.warning("Empty resume text provided to predict()")
            raise ValueError("resume_text cannot be empty")
        
        try:
            if not self.is_trained:
                logger.info("Model not trained yet, training now")
                self.train()

            # Prepare input: combine resume text with skills (weighted)
            input_text = f"{resume_text.lower()}"
            if skills:
                input_text += f" {' '.join(str(s) for s in skills if s) * 3}"

            logger.debug(f"Predicting role for resume with {len(input_text)} characters")

            # Vectorize
            input_vec = self.vectorizer.transform([input_text])

            # Get prediction and probabilities
            predicted_label = self.model.predict(input_vec)[0]
            predicted_role = self.label_encoder.inverse_transform([predicted_label])[0]

            # Get probabilities
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(input_vec)[0]
            else:
                # For models without predict_proba
                probabilities = np.zeros(len(self.classes))
                probabilities[predicted_label] = 1.0

            # Build probability map
            prob_map: Dict[str, float] = {}
            for i, role in enumerate(self.classes):
                prob_map[role] = round(float(probabilities[i]) * 100, 1)

            # Sort by probability
            sorted_probs = dict(sorted(prob_map.items(), key=lambda x: x[1], reverse=True))

            logger.info(f"Predicted role: {predicted_role} with {sorted_probs[predicted_role]}% confidence")

            return {
                "predicted_role": predicted_role,
                "confidence": round(float(probabilities[predicted_label]) * 100, 1),
                "all_probabilities": sorted_probs,
                "top_3_roles": list(sorted_probs.items())[:3],
                "model_type": self.model_type,
                "model_accuracy": round(self.training_accuracy * 100, 1)
            }
        except Exception as e:
            logger.error(f"Error predicting role: {e}")
            return {
                "error": str(e),
                "predicted_role": "Unknown",
                "confidence": 0.0,
                "all_probabilities": {},
                "top_3_roles": [],
                "model_type": self.model_type
            }

    def get_feature_importance(self, resume_text: str, skills: Optional[List[str]] = None, top_n: int = 10) -> List[Dict[str, object]]:
        """
        Get the most influential features (skills/keywords) for the prediction.
        Implements Explainable AI for the recommendation.

        Args:
            resume_text: Resume text
            skills: Optional extracted skills list
            top_n: Number of top features to return (1-20 recommended)

        Returns:
            List of feature importance dicts with feature names and scores
            
        Raises:
            ValueError: If top_n is invalid
        """
        if not resume_text or not resume_text.strip():
            logger.warning("Empty resume text provided to get_feature_importance()")
            return []
        
        if top_n < 1 or top_n > 50:
            logger.warning(f"Invalid top_n: {top_n}, using default of 10")
            top_n = 10
        
        try:
            if not self.is_trained:
                logger.debug("Model not trained, returning empty importance list")
                return []

            input_text = f"{resume_text.lower()}"
            if skills:
                input_text += f" {' '.join(str(s) for s in skills if s) * 3}"
            
            input_vec = self.vectorizer.transform([input_text])

            feature_names = self.vectorizer.get_feature_names_out()
            input_array = input_vec.toarray()[0]

            # For Logistic Regression: use coefficient magnitude
            if hasattr(self.model, 'coef_') and self.model_type == "logistic_regression":
                predicted_class = self.model.predict(input_vec)[0]
                coefficients = self.model.coef_[predicted_class]
                importance_scores = input_array * np.abs(coefficients)
            else:
                # Fall back to TF-IDF scores
                importance_scores = input_array

            # Get top features
            top_indices = np.argsort(importance_scores)[-top_n:][::-1]

            features: List[Dict[str, object]] = []
            skill_set = {s.lower() for s in (skills or []) if s}
            
            for idx in top_indices:
                if idx < len(feature_names) and importance_scores[idx] > 0:
                    features.append({
                        "feature": str(feature_names[idx]),
                        "score": round(float(importance_scores[idx]), 4),
                        "is_skill": feature_names[idx] in skill_set
                    })

            logger.debug(f"Extracted {len(features)} important features")
            return features
        except Exception as e:
            logger.error(f"Error computing feature importance: {e}")
            return []


def get_role_predictor(model_type: str = DEFAULT_MODEL_TYPE) -> RolePredictor:
    """
    Factory function to get a trained RolePredictor instance.

    Args:
        model_type: Model type to use

    Returns:
        Trained RolePredictor
    """
    predictor = RolePredictor(model_type=model_type)
    predictor.train()
    return predictor
