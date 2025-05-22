from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(1), nullable=False)        # 'M' lub 'K'
    weight = db.Column(db.Float, nullable=False)            # waga w kg (wartości numeryczne)
    height = db.Column(db.Float, nullable=False)            # wzrost w cm (wartości numeryczne)
    bmi = db.Column(db.Float, nullable=False)               # BMI (wartości numeryczne)
    CRP = db.Column(db.Float, nullable=False)               # CRP (wartości numeryczne)
    Alb = db.Column(db.Float, nullable=False)               # Alb (wartości numeryczne)
    WCC = db.Column(db.Float, nullable=False)               # WCC (wartości numeryczne)
    NEU = db.Column(db.Float, nullable=False)               # NEU (wartości numeryczne)
    total_protein = db.Column(db.Float, nullable=False)     # białko całkowite (wartości numeryczne)
    pT = db.Column(db.String(10), nullable=False)           # stadium T (wartości kategoryczne)
    pN = db.Column(db.String(10), nullable=False)           # stadium N (wartości kategoryczne)
    pM = db.Column(db.String(10), nullable=False)           # stadium M (wartości kategoryczne)
    PNI = db.Column(db.Integer, nullable=False)             # PNI (wartości numeryczne 0-1)
    GRADING = db.Column(db.String(10), nullable=False)      # stopień zróżnicowania (wartości kategoryczne) 
    Lauren = db.Column(db.String(10), nullable=False)       # typ Lauren (wartości kategoryczne)
    CTH_preop = db.Column(db.String(10), nullable=False)    # chemioterapia przedoperacyjna (wartości kategoryczne)
    cycles_number = db.Column(db.Integer, nullable=False)   # liczba cykli chemioterapii (wartości numeryczne)
    
    leukocytes = db.Column(db.Float, nullable=True)        # NEW: total leukocytes count (nullable)
    pni_float = db.Column(db.Float, nullable=True)         # NEW: float PNI value (nullable)
    
    predictions = db.relationship('Prediction', backref='patient', lazy=True)

    def __repr__(self):
        return f'<Patient {self.id} - {self.age}y {self.gender}>'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)
    interpretation = db.Column(db.String(50), nullable=False)
    top_factors = db.Column(db.JSON)  # Stores list of important factors

    clinician_agreement = db.Column(db.String(20))  # 'agree', 'disagree', 'ambivalent'
    clinician_notes = db.Column(db.Text)
    
    # Relationship
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    def __repr__(self):
        return f'<Prediction {self.id} for Patient {self.patient_id}>'