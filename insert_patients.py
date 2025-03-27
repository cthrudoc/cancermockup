import random
from models import db, Patient
from app import create_app

app = create_app()

def generate_mock_patients(num_patients=40):
    surgical_approaches = ["Open", "Laparoscopic", "Robotic", "Thoracoscopic"]
    lymphadenectomy_options = ["None", "Sentinel", "Regional", "Extended"]
    asa_classes = ["I", "II", "III", "IV", "V"]
    gender_options = ["Male", "Female"]
    
    with app.app_context():
        # Clear existing patients
        db.session.query(Patient).delete()
        
        for i in range(1, num_patients + 1):
            patient = Patient(
                age=random.randint(30, 85),
                gender=random.choice(gender_options),
                bmi_all=round(random.uniform(18.5, 40.0), 1),
                surgical_duration=random.randint(30, 300),
                surgical_approach=random.choice(surgical_approaches),
                lymphadenectomy=random.choice(lymphadenectomy_options),
                asa_classification=random.choice(asa_classes),
                tumor_size=round(random.uniform(0.5, 10.0), 1),
                ct=f"cT{random.randint(1, 4)}",
                cn=f"cN{random.randint(0, 2)}",
                pt=f"pT{random.randint(1, 4)}",
                pn=f"pN{random.randint(0, 2)}",
                cci=random.randint(0, 5)
            )
            db.session.add(patient)
        
        db.session.commit()
        print(f"Successfully added {num_patients} patients with correct fields")

if __name__ == '__main__':
    generate_mock_patients()