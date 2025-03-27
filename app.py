from flask import Flask, render_template, request
from models import db, Patient
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cancer_ops.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'  # Change in production
    
    # Initialize database
    db.init_app(app)
    
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
                (Patient.ct.contains(search_query)) | 
                (Patient.cn.contains(search_query)) |
                (Patient.asa_classification.contains(search_query)) |
                (Patient.gender.contains(search_query))
            )
        
        # Add sorting logic
        if sort_by == 'age':
            sort_column = Patient.age
        elif sort_by == 'id':
            sort_column = Patient.id
        elif sort_by == 'tumor_size':
            sort_column = Patient.tumor_size
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
        return render_template('patient.html', patient=patient)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)