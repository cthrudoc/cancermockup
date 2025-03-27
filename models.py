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