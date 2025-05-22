import csv
from app import create_app
from models import db, Patient, Prediction
from ml_models import MLModel
import traceback

app = create_app()
ml_model = MLModel()

def process_csv_row(row):
    """Convert CSV row to proper data types and format"""
    processed = {}
    
    # Handle numeric fields with comma as decimal separator
    for key in row:
        if key in ['WIEK W DNIU OPERACJI', 'waga', 'wzrost', 'BMI', 'CRP', 'Alb', 
                  'WCC', 'NEU', 'białko całkowite', 'LICZBA CYKLI']:
            value = row[key].replace(',', '.') if isinstance(row[key], str) else str(row[key])
            processed[key] = float(value)
        elif key == 'PNI (perineural invasion)':
            processed[key] = int(float(row[key]))
        else:
            processed[key] = row[key]
    
    # Add default values for new fields
    processed['leukocytes'] = None  # Default value, adjust as needed
    processed['pni_float'] = None  # Default value, adjust as needed
    
    return processed
def insert_patients_from_csv(csv_path):
    with app.app_context():
        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        processed_row = process_csv_row(row)
                        
                        # Create patient
                        patient = Patient(
                            gender=processed_row['PŁEĆ'],
                            weight=processed_row['waga'],
                            height=processed_row['wzrost'],
                            bmi=processed_row['BMI'],
                            CRP=processed_row['CRP'],
                            Alb=processed_row['Alb'],
                            WCC=processed_row['WCC'],
                            NEU=processed_row['NEU'],
                            total_protein=processed_row['białko całkowite'],
                            pT=processed_row['pT'],
                            pN=processed_row['pN'],
                            pM=processed_row['pM'],
                            PNI=processed_row['PNI (perineural invasion)'],
                            GRADING=processed_row['GRADING'],
                            Lauren=processed_row['Lauren'],
                            CTH_preop=processed_row['CTH przedoperacyjna'],
                            cycles_number=int(processed_row['LICZBA CYKLI'])
                        )
                        
                        db.session.add(patient)
                        db.session.flush()  # Get the ID before commit
                        
                        # Prepare input data for prediction
                        input_data = {
                            'WIEK W DNIU OPERACJI': int(processed_row['WIEK W DNIU OPERACJI']),
                            'PŁEĆ': processed_row['PŁEĆ'],
                            'waga': processed_row['waga'],
                            'wzrost': processed_row['wzrost'],
                            'BMI': processed_row['BMI'],
                            'CRP': processed_row['CRP'],
                            'Alb': processed_row['Alb'],
                            'WCC': processed_row['WCC'],
                            'NEU': processed_row['NEU'],
                            'białko całkowite': processed_row['białko całkowite'],
                            'pT': processed_row['pT'],
                            'pN': processed_row['pN'],
                            'pM': processed_row['pM'],
                            'PNI (perineural invasion)': processed_row['PNI (perineural invasion)'],
                            'GRADING': processed_row['GRADING'],
                            'Lauren': processed_row['Lauren'],
                            'CTH przedoperacyjna': processed_row['CTH przedoperacyjna'],
                            'LICZBA CYKLI': int(processed_row['LICZBA CYKLI'])
                        }
                        
                        # Make prediction with all available models
                        for model_name in ['Random Forest', 'XGBoost', 'CatBoost']:
                            try:
                                result = ml_model.predict(input_data, model_name)
                                
                                prediction = Prediction(
                                    patient_id=patient.id,
                                    probability=result['probability'],
                                    model_used=model_name,
                                    interpretation=result['interpretation'],
                                    top_factors=result['vars_importance']
                                )
                                db.session.add(prediction)
                            except Exception as e:
                                print(f"Error predicting with {model_name} for patient {patient.id}: {str(e)}")
                                continue
                        
                        db.session.commit()
                        print(f"Successfully added patient {patient.id}")
                        
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error processing patient row: {str(e)}")
                        print(traceback.format_exc())
                        continue
                        
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            print(traceback.format_exc())

if __name__ == '__main__':
    print("Starting patient import...")
    insert_patients_from_csv('filtered_patients2.csv')
    print("Patient import completed!")