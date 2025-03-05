import os

class Config:
    """Configuration settings for the Flask application."""
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat_history.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable to avoid performance overhead