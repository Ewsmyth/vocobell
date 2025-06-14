from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    theme = db.Column(db.Boolean(), nullable=False, default=False)
    first_login = db.Column(db.Boolean(), default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_id(self):
        return str(self.user_id)

class SoundFile(db.Model):
    sound_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sound_name = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(500), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id = db.relationship('User')

class Webhook(db.Model):
    webhook_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    webhook_name = db.Column(db.String(255), nullable=False)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    sound_file_id = db.Column(db.Integer, db.ForeignKey('sound_file.sound_id'), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sound_file = db.relationship('SoundFile')
    owner_id = db.relationship('User')
