import pickle
from pathlib import Path

def test_model_loading():
    try:
        print("\n=== Testing Model Loading ===")
        model_path = Path("model_files/XGBoost_model.pkl")
        print(f"Model exists: {model_path.exists()}")
        print(f"File size: {model_path.stat().st_size} bytes")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            print("Model loaded successfully!")
            print(f"Model type: {type(model)}")
            
            # Try a dummy prediction
            try:
                dummy_input = [[1]*len(model.feature_names_in_)]  # Adjust based on actual features
                pred = model.predict_proba(dummy_input)
                print(f"Dummy prediction succeeded: {pred}")
            except Exception as e:
                print(f"Dummy prediction failed: {str(e)}")
                
    except Exception as e:
        print(f"Model loading failed: {str(e)}")

if __name__ == '__main__':
    test_model_loading()