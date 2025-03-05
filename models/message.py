from datetime import datetime, timezone
from extensions import db

class Message(db.Model):
    """Model for storing chat messages."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    role = db.Column(db.String(10))
    content = db.Column(db.Text)