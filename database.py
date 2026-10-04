
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    complaint_text = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(100))
    priority = db.Column(db.String(20))
    priority_score = db.Column(db.Integer)

    department = db.Column(db.String(100))

    status = db.Column(
        db.String(30),
        default="Submitted"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Complaint {self.id}>"
