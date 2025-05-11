from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    bmi_all = db.Column(db.Float, nullable=False)
    surgical_duration = db.Column(db.Integer, nullable=False)  # in minutes
    surgical_approach = db.Column(db.String(50), nullable=False)
    lymphadenectomy = db.Column(db.String(20), nullable=False)
    asa_classification = db.Column(db.String(10), nullable=False)
    tumor_size = db.Column(db.Float, nullable=False)  # maximum diameter in cm
    ct = db.Column(db.String(10), nullable=False)    # clinical T stage
    cn = db.Column(db.String(10), nullable=False)    # clinical N stage
    pt = db.Column(db.String(10))                   # pathological T stage
    pn = db.Column(db.String(10))                   # pathological N stage
    cci = db.Column(db.Integer, nullable=False)     # Charlson Comorbidity Index

    def __repr__(self):
        return f'<Patient {self.id} - {self.age}y {self.gender}>'

class Test(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(1), nullable=False)       # 'M' lub 'K'
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
    PNI = db.Column(db.Integer, nullable=False)         # PNI (wartości numeryczne 0-1)
    GRADING = db.Column(db.String(10), nullable=False)      # stopień zróżnicowania (wartości kategoryczne) 
    Lauren = db.Column(db.String(10), nullable=False)       # typ Lauren (wartości kategoryczne)
    CTH_preop = db.Column(db.String(10), nullable=False)    # chemioterapia przedoperacyjna (wartości kategoryczne)
    cycles_number = db.Column(db.Integer, nullable=False)   # liczba cykli chemioterapii (wartości numeryczne)

    def __repr__(self):
        return f'<Patient {self.id} - {self.age}y {self.gender}>'
