from flask import request, jsonify, current_app
from extensions import db
from models.message import Message
from services.openai_service import get_completion
import uuid
from datetime import datetime, timezone

def openai_completion():
    data = request.get_json()
    prompt = data.get('prompt')
    user_id = data.get('user_id')
    
    # Validate input
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    # Generate user_id if not provided
    if not user_id:
        user_id = str(uuid.uuid4())
    
    # Retrieve conversation history
    history = Message.query.filter_by(user_id=user_id).order_by(Message.timestamp).all()
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": prompt})
    
    # Get response from openai
    try:
        completion = get_completion(messages)
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request'}), 500
    
    # Save messages to database
    timestamp = datetime.now(timezone.utc)
    user_message = Message(user_id=user_id, timestamp=timestamp, role="user", content=prompt)
    assistant_message = Message(user_id=user_id, timestamp=timestamp, role="assistant", content=completion)
    db.session.add(user_message)
    db.session.add(assistant_message)
    db.session.commit()
    
    return jsonify({'user_id': user_id, 'completion': completion}), 200