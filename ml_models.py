import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import pickle

class MLModel:
    def __init__(self):
        self.models = {}
        self.loaded = False
        self.grade_classes = ['I', 'II', 'III', 'IV']  # Grade classes
        self.grade_descriptions = {
            'I': 'LOW RISK',
            'II': 'MODERATE RISK',
            'III': 'HIGH RISK',
            'IV': 'VERY HIGH RISK'
        }
    
    def load_models(self):
        try:
            print("Ładowanie modeli i obiektów preprocessingu...")
            self.models = {
                'Random Forest': self._load_latest_model("Random_Forest_model"),
                'XGBoost': self._load_latest_model("XGBoost_model"),
                'CatBoost': self._load_latest_model("CatBoost_model")
            }

            # Load preprocessing objects
            preprocessing_path = os.path.join("ModelsGrade", "preprocessing_objects.pkl")
            preprocessing = joblib.load(preprocessing_path)
            self.imputer = preprocessing['imputer']
            self.label_encoders = preprocessing['label_encoders']
            self.feature_names = preprocessing['feature_names']
            
            print("Modele i obiekty preprocessingu zostały wczytane pomyślnie!")
            self.loaded = True
            return True
            
        except Exception as e:
            print(f"Błąd podczas wczytywania modeli: {str(e)}")
            raise

    def _load_latest_model(self, model_name, directory="ModelsGrade"):
        """Loads the latest model of given type from specified directory"""
        files = [f for f in os.listdir(directory) if f.startswith(model_name)]
        if not files:
            raise FileNotFoundError(f"No {model_name} models found in {directory}")
        latest_file = max(files)
        filepath = os.path.join(directory, latest_file)
        return joblib.load(filepath)

    def predict(self, input_data, selected_model_name='Random Forest'):
        if not self.loaded:
            if not self.load_models():
                raise Exception("Models failed to load")

        try:
            # Prepare input data
            processed_data = {}
            for feature in self.feature_names:
                if feature in self.label_encoders:
                    # For categorical features
                    le = self.label_encoders[feature]
                    if input_data[feature] not in le.classes_:
                        processed_data[feature] = le.transform([le.classes_[0]])[0]
                    else:
                        processed_data[feature] = le.transform([input_data[feature]])[0]
                else:
                    # For numerical features
                    processed_data[feature] = input_data[feature]

            # Create DataFrame
            input_df = pd.DataFrame([processed_data], columns=self.feature_names)

            # Impute missing values
            input_df = pd.DataFrame(self.imputer.transform(input_df), columns=self.feature_names)

            # Get selected model
            selected_model = self.models[selected_model_name]
            
            # Make prediction
            probabilities = selected_model.predict_proba(input_df)[0]
            predicted_class_idx = np.argmax(probabilities)
            predicted_grade = self.grade_classes[predicted_class_idx]
            predicted_prob = probabilities[predicted_class_idx]
            
            # Get top factors
            top_factors = []
            if hasattr(selected_model, 'feature_importances_'):
                importances = dict(zip(self.feature_names, selected_model.feature_importances_))
                importances = self._normalize_importance(importances)
                top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:3]
                top_factors = [f"{feature}: {importance:.2f}%" for feature, importance in top_features]
            elif hasattr(selected_model, 'coef_'):
                coef = dict(zip(self.feature_names, selected_model.coef_[0]))
                coef = self._normalize_importance(coef)
                top_features = sorted(coef.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
                top_factors = [f"{feature}: {abs(importance):.2f}%" for feature, importance in top_features]
            elif hasattr(selected_model, 'get_feature_importance'):
                raw_importances = selected_model.get_feature_importance()
                importances = dict(zip(self.feature_names, raw_importances))
                importances = self._normalize_importance(importances)
                top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:3]
                top_factors = [f"{feature}: {importance:.2f}%" for feature, importance in top_features]
            
            return {
                'probability': predicted_prob,
                'grade': predicted_grade,
                'interpretation': self.grade_descriptions[predicted_grade],
                'model_used': selected_model_name,
                'vars_importance': top_factors,
                'all_probabilities': {grade: prob for grade, prob in zip(self.grade_classes, probabilities)}
            }

        except Exception as e:
            print(f"\nError during data processing: {str(e)}")
            print("\nCheck if all required variables are properly defined:")
            for i, feature in enumerate(self.feature_names, 1):
                print(f"{i}. {feature}")
            raise Exception(f'[MLModel.predict] Error: {str(e)}')

    def _normalize_importance(self, importance_values):
        total = sum(abs(x) for x in importance_values.values())
        return {k: (v/total)*100 for k, v in importance_values.items()}