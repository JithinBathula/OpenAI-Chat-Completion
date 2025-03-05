from flask import Flask
from extensions import db
from routes.openai_routes import openai_bp



# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

# Register routes
app.register_blueprint(openai_bp)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)