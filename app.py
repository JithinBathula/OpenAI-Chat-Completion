from flask import Flask, jsonify
from extensions import db, limiter
from routes.openai_routes import openai_bp

# initialize flask app
app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
limiter.init_app(app)

# register routes
app.register_blueprint(openai_bp)

@app.errorhandler(429)
def rate_limit_exceeded(e):
    response = jsonify({
        "error": "Rate limit exceeded",
        "message": str(e.description),
    })
    response.status_code = 429
    return response



# create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)