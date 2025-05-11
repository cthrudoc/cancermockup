import pickle
import pandas as pd
import numpy as np
import sklearn


# Wczytanie modeli i obiektów preprocessingu
try:
    models = {}
    model_files = {
        'Random Forest': 'Random_Forest_model.pkl',
        'XGBoost': 'XGBoost_model.pkl',
        'CatBoost': 'CatBoost_model.pkl'
    }

    for name, file in model_files.items():
        with open(file, 'rb') as f:
            models[name] = pickle.load(f)

    with open('preprocessing_objects.pkl', 'rb') as f:
        preprocessing = pickle.load(f)
        imputer = preprocessing['imputer']
        label_encoders = preprocessing['label_encoders']
        feature_names = preprocessing['feature_names']

    print("Modele i obiekty preprocessingu zostały wczytane pomyślnie!")
except Exception as e:
    # print(f"Błąd podczas wczytywania modeli: {e}")
    raise

# wprowadź  dane do predykcji
# Wypełnij wartościami odpowiednich zmiennych
input_data = {
    'WIEK W DNIU OPERACJI': 65,          # wiek w latach (wartości numeryczne)
    'PŁEĆ': 'M',                         # 'M' lub 'K'
    'waga': 70.0,                        # waga w kg (wartości numeryczne)
    'wzrost': 175.0,                     # wzrost w cm (wartości numeryczne)
    'BMI': 22.9,                         # BMI (wartości numeryczne)
    'CRP': 105.2,                          # CRP (wartości numeryczne)
    'Alb': 4.2,                          # Alb (wartości numeryczne)
    'WCC': 7.5,                          # WCC (wartości numeryczne)
    'NEU': 4.5,                          # NEU (wartości numeryczne)
    'białko całkowite': 6.9,             # białko całkowite (wartości numeryczne)
    'pT': 'T2',                          # stadium T (wartości kategoryczne)
    'pN': 'N0',                          # stadium N (wartości kategoryczne)
    'pM': 'M0',                          # stadium M (wartości kategoryczne)
    'PNI (perineural invasion)': 0.2,     # PNI (wartości numeryczne 0-1)
    'GRADING': 'G2',                     # stopień zróżnicowania (wartości kategoryczne)
    'Lauren': 'jelitowy',                # typ Lauren (wartości kategoryczne)
    'CTH przedoperacyjna': 'tak',         # chemioterapia przedoperacyjna (wartości kategoryczne)
    'LICZBA CYKLI': 4.0,                 # liczba cykli chemioterapii (wartości numeryczne)
}

# Wybór modelu (możesz zmienić na 'XGBoost' lub 'CatBoost')
selected_model_name = 'Random Forest'

# 4. Przetwarzanie danych i predykcja
try:
    # Przygotowanie danych wejściowych
    processed_data = {}
    for feature in feature_names:
        if feature in label_encoders:
            # Dla cech kategorycznych - sprawdź czy wartość jest w dopuszczalnych
            le = label_encoders[feature]
            if input_data[feature] not in le.classes_:
                # # Jeśli wartość nie jest w dopuszczalnych, użyj pierwszej dostępnej
                # print(f"Uwaga: Wartość '{input_data[feature]}' dla cechy '{feature}' nie jest w dopuszczalnych wartościach: {le.classes_}. Używam domyślnej wartości.")
                processed_data[feature] = le.transform([le.classes_[0]])[0]
            else:
                processed_data[feature] = le.transform([input_data[feature]])[0]
        else:
            # Dla cech numerycznych - użyj bezpośrednio wartości
            processed_data[feature] = input_data[feature]

    # Tworzenie DataFrame
    input_df = pd.DataFrame([processed_data], columns=feature_names)

    # Uzupełnianie brakujących wartości
    input_df = pd.DataFrame(imputer.transform(input_df), columns=feature_names)

    # Wybór modelu
    selected_model = models[selected_model_name]

    # Predykcja
    probability = selected_model.predict_proba(input_df)[0][1]

    # Wyświetlanie wyniku
    print(f"\nWybrany model: {selected_model_name}")
    print(f"Prawdopodobieństwo powikłań pooperacyjnych: {probability*100:.2f}%")

    # Interpretacja wyniku
    if probability > 0.7:
        print("\nINTERPRETACJA: WYSOKIE RYZYKO POWIKŁAŃ")
        print("Zalecenia: Konieczność szczególnego monitorowania, rozważenie dodatkowych środków ostrożności")
    elif probability > 0.4:
        print("\nINTERPRETACJA: UMIARKOWANE RYZYKO POWIKŁAŃ")
        print("Zalecenia: Standardowe monitorowanie pooperacyjne")
    else:
        print("\nINTERPRETACJA: NISKIE RYZYKO POWIKŁAŃ")
        print("Zalecenia: Rutynowa obserwacja pooperacyjna")

    # Dodatkowe informacje
    print("\nTop 3 najważniejsze czynniki wpływające na predykcję:")
    if hasattr(selected_model, 'feature_importances_'):
        importances = pd.Series(selected_model.feature_importances_, index=feature_names)
        top_features = importances.sort_values(ascending=False).head(3)
        for i, (feature, importance) in enumerate(top_features.items(), 1):
            print(f"{i}. {feature}: {importance:.4f}")
    elif hasattr(selected_model, 'coef_'):
        coef = pd.Series(selected_model.coef_[0], index=feature_names)
        top_features = coef.abs().sort_values(ascending=False).head(3)
        for i, (feature, coef_value) in enumerate(top_features.items(), 1):
            print(f"{i}. {feature}: {coef_value:.4f}")

except Exception as e:
    print(f"\nWystąpił błąd podczas przetwarzania danych: {str(e)}")
    print("\nSprawdź czy wszystkie wymagane zmienne zostały poprawnie zdefiniowane:")
    for i, feature in enumerate(feature_names, 1):
        print(f"{i}. {feature}")