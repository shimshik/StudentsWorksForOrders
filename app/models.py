from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)  # увеличено для scrypt

    def __repr__(self):
        return f"<User {self.email}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Shipment(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(64), unique=True, nullable=False)
    origin = db.Column(db.String(128), nullable=False)
    destination = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(64), nullable=False, default='В пути')
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Shipment {self.tracking_number}>"


class ContactRequest(db.Model):
    __tablename__ = 'contact_requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')  # new, in_progress, completed

    def __repr__(self):
        return f'<ContactRequest {self.name} - {self.email}>'