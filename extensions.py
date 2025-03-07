# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# database
db = SQLAlchemy()

# limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"] 
)