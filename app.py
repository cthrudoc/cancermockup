from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Patient, Prediction
import os 
from ml_models import MLModel  
from flask_migrate import Migrate
import traceback

ml_model = MLModel()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cancer_ops.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'  # Change in production
    
    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Routes
    @app.route('/')
    def index():
        search_query = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        per_page = 10
        sort_by = request.args.get('sort', 'id')  # Default sort by ID
        sort_order = request.args.get('order', 'asc')  # Default ascending
        
        base_query = Patient.query
        
        if search_query:
            base_query = base_query.filter(
                (Patient.gender.contains(search_query)) |
                (Patient.pT.contains(search_query)) |
                (Patient.pN.contains(search_query)) |
                (Patient.GRADING.contains(search_query)) |
                (Patient.Lauren.contains(search_query))
            )
        
        # Add sorting logic for new fields
        if sort_by == 'weight':
            sort_column = Patient.weight
        elif sort_by == 'height':
            sort_column = Patient.height
        elif sort_by == 'bmi':
            sort_column = Patient.bmi
        elif sort_by == 'CRP':
            sort_column = Patient.CRP
        elif sort_by == 'Alb':
            sort_column = Patient.Alb
        elif sort_by == 'pT':
            sort_column = Patient.pT
        elif sort_by == 'pN':
            sort_column = Patient.pN
        elif sort_by == 'id':
            sort_column = Patient.id
        else:  # Default case
            sort_column = Patient.id
        
        # Apply sort order
        if sort_order == 'desc':
            patients = base_query.order_by(sort_column.desc())
        else:
            patients = base_query.order_by(sort_column.asc())
        
        patients = patients.paginate(page=page, per_page=per_page)
        
        return render_template('index.html', 
                            patients=patients, 
                            search_query=search_query,
                            sort_by=sort_by,
                            sort_order=sort_order)
    
    @app.route('/patient/<int:patient_id>')
    def patient_detail(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        predictions = patient.predictions
        return render_template('patient.html', patient=patient, predictions=predictions)
    
    @app.route('/patient/<int:patient_id>/predict', methods=['GET', 'POST'])
    def predict_complications(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        
        if request.method == 'POST':
            try:
                # Prepare input data from form
                input_data = {
                    'WIEK W DNIU OPERACJI': int(request.form.get('age', patient.age)),
                    'PŁEĆ': request.form.get('gender', patient.gender[0]),
                    'waga': float(request.form.get('weight', 70.0)),
                    'wzrost': float(request.form.get('height', 170.0)),
                    'BMI': float(request.form.get('bmi', patient.bmi)),
                    'CRP': float(request.form.get('crp', 5.0)),
                    'Alb': float(request.form.get('alb', 4.0)),
                    'WCC': float(request.form.get('wcc', 7.0)),
                    'NEU': float(request.form.get('neu', 4.0)),
                    'białko całkowite': float(request.form.get('total_protein', 6.5)),
                    'pT': request.form.get('pt', patient.pT),
                    'pN': request.form.get('pn', patient.pN),
                    'pM': request.form.get('pm', 'M0'),
                    'PNI (perineural invasion)': int(request.form.get('pni', 0)),
                    'GRADING': request.form.get('grading', 'G2'),
                    'Lauren': request.form.get('lauren', 'jelitowy'),
                    'CTH przedoperacyjna': request.form.get('cth_preop', 'nie'),
                    'LICZBA CYKLI': int(request.form.get('cycles', 0))
                }
                
                model_name = request.form.get('model', 'Random Forest')
                result = ml_model.predict(input_data, model_name)
                
                # Add pre-calculated percentage for cleaner template
                result['probability_percent'] = round(result['probability'] * 100, 1)
                
                return render_template('patient.html', 
                                    patient=patient,
                                    prediction_result=result)
                
            except Exception as e:
                flash(f'Prediction error: {str(e)}', 'error')
                return redirect(url_for('patient_detail', patient_id=patient_id))
        
        return render_template('prediction_form.html', patient=patient)
    
    @app.route('/patient/new', methods=['GET', 'POST'])
    def new_patient():
        if request.method == 'POST':
            try:

                print("[DEBUG] Starting patient creation.")

                pni_float = request.form.get('pni_float')
                pni_value = 1 if pni_float and float(pni_float) > 45 else 0

                # Create new patient
                patient = Patient(
                    gender=request.form['gender'],
                    weight=float(request.form['weight']),
                    height=float(request.form['height']),
                    bmi=float(request.form['bmi']),
                    CRP=float(request.form['crp']),
                    Alb=float(request.form['alb']),
                    WCC=float(request.form['wcc']),
                    NEU=float(request.form['neu']),
                    total_protein=float(request.form['total_protein']),
                    pT=request.form['pt'],
                    pN=request.form['pn'],
                    pM=request.form['pm'],
                    GRADING=request.form['grading'],
                    Lauren=request.form['lauren'],
                    CTH_preop=request.form['cth_preop'],
                    cycles_number=int(request.form['cycles']),
                    leukocytes=float(request.form['leukocytes']) if request.form.get('leukocytes') else None, 
                    pni_float=float(pni_float) if pni_float else None,  
                    PNI = pni_value,
                    )
                    
                db.session.add(patient)
                db.session.flush()  # Get the ID before commit

                print(f"[DEBUG] Patient created with ID {patient.id}")

                # Make prediction

                print("[DEBUG] Preparing input data...")

                input_data = {
                    'WIEK W DNIU OPERACJI': int(request.form['age']),
                    'PŁEĆ': request.form['gender'],
                    'waga': float(request.form['weight']),
                    'wzrost': float(request.form['height']),
                    'BMI': float(request.form['bmi']),
                    'CRP': float(request.form['crp']),
                    'Alb': float(request.form['alb']),
                    'WCC': float(request.form['wcc']),
                    'NEU': float(request.form['neu']),
                    'białko całkowite': float(request.form['total_protein']),
                    'pT': request.form['pt'],
                    'pN': request.form['pn'],
                    'pM': request.form['pm'],
                    'PNI (perineural invasion)': pni_value,  # Use the calculated binary PNI value
                    'GRADING': request.form['grading'],
                    'Lauren': request.form['lauren'],
                    'CTH przedoperacyjna': request.form['cth_preop'],
                    'LICZBA CYKLI': int(request.form['cycles'])
                }
                print("[DEBUG] Input data recieved :")
                print(f'{input_data}')

                # Make predictions with all models
                model_names = ['Random Forest', 'XGBoost', 'CatBoost']
                predictions_created = 0
                for model_name in model_names:
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
                        predictions_created += 1
                    except Exception as e:
                        print(f"Error predicting with {model_name}: {str(e)}")
                        continue

                if predictions_created == 0:
                    raise Exception("Failed to create any predictions")
                
                db.session.commit()
                flash('New patient and prediction added successfully!', 'success')
                return redirect(url_for('patient_detail', patient_id=patient.id))
                
            except Exception as e:
                print(f"[!!!] [ERROR] : {e}")
                print("[DEBUG] Full error:", traceback.format_exc())
                db.session.rollback()
                flash(f'Error: {str(e)}', 'danger')
                return redirect(url_for('new_patient'))
        
        # GET request - show empty form
        return render_template('new_patient.html')

    @app.route('/prediction/<int:prediction_id>/feedback', methods=['POST'])
    def save_feedback(prediction_id):
        prediction = Prediction.query.get_or_404(prediction_id)
        if request.method == 'POST':
            prediction.clinician_agreement = request.form.get('agreement')
            prediction.clinician_notes = request.form.get('clinician_notes', '')
            db.session.commit()
            flash('Feedback saved successfully', 'success')
        return redirect(url_for('patient_detail', patient_id=prediction.patient_id))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)