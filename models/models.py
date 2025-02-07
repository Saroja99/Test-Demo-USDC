from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Demo(db.Model):
    __tablename__ = 'Demo'  # Specify the table name (use this in case the table name doesn't match the class name)
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Relationship for easy access to scores
    scores = db.relationship('DemoScore', backref='demo', lazy=True)

class DemoScore(db.Model):
    __tablename__ = 'DemoScores'  # Specify the table name
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Demo.id'), nullable=False)  # Foreign key to Demo
    score = db.Column(db.Integer, nullable=False)
