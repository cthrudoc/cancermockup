import random
from models import db, Patient
from app import create_app

app = create_app()

def generate_mock_patients(num_patients=40):
    gender_options = ["M", "K"]
    pT_stages = ["T1", "T2", "T3", "T4"]
    pN_stages = ["N0", "N1", "N2", "N3"]
    pM_stages = ["M0", "M1"]
    grading_options = ["G1", "G2", "G3"]
    lauren_types = ["jelitowy", "rozsiany", "mieszany"]
    cth_preop_options = ["tak", "nie"]
    
    with app.app_context():
        # Clear existing patients
        # db.session.query(Patient).delete()
        
        for i in range(1, num_patients + 1):
            patient = Patient(
                gender=random.choice(gender_options),
                weight=round(random.uniform(50, 120), 1),
                height=random.randint(150, 200),
                bmi=round(random.uniform(18.5, 40.0), 1),
                CRP=round(random.uniform(0.1, 200.0), 1),
                Alb=round(random.uniform(2.5, 5.5), 1),
                WCC=round(random.uniform(2.0, 20.0), 1),
                NEU=round(random.uniform(1.0, 15.0), 1),
                total_protein=round(random.uniform(5.0, 8.5), 1),
                pT=random.choice(pT_stages),
                pN=random.choice(pN_stages),
                pM=random.choice(pM_stages),
                PNI=random.randint(0, 1),
                GRADING=random.choice(grading_options),
                Lauren=random.choice(lauren_types),
                CTH_preop=random.choice(cth_preop_options),
                cycles_number=random.randint(0, 6)
            )
            db.session.add(patient)
        
        db.session.commit()
        print(f"Successfully added {num_patients} patients with new fields")

if __name__ == '__main__':
    generate_mock_patients()