from flask import Blueprint
from controllers.openai_controller import openai_completion
from extensions import limiter

# Define the blueprint
openai_bp = Blueprint('openai', __name__)

@openai_bp.route('/openai-completion', methods=['POST'])
@limiter.limit("10 per minute")
def openai_completion_route():
    return openai_completion()