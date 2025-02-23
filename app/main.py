import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask app
app = Flask(__name__)
app.config.from_object("config.Config")
CORS(app)

# Database setup
db = SQLAlchemy(app)

# Rate limiter setup
limiter = Limiter(get_remote_address)
limiter.init_app(app)

# Load API Key from environment variables
API_KEY = os.getenv("API_KEY")

# Model for storing subscribers
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.before_first_request
def create_tables():
    """Ensure database tables exist."""
    db.create_all()

def verify_api_key():
    """Verify if the request contains a valid API key."""
    request_api_key = request.headers.get("X-API-Key")
    if not API_KEY or request_api_key != API_KEY:
        return False
    return True

@app.route("/subscribe", methods=["POST"])
@limiter.limit("5 per minute")  # ⏳ Limit to 5 requests per minute
def subscribe():
    """Handle newsletter subscriptions securely."""
    
    # 🔒 Require API Key
    if not verify_api_key():
        return jsonify({"error": "Unauthorized request"}), 403  # 🚨 Reject unauthorized requests

    email = request.form.get("email")
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Check if email already exists
    existing_subscriber = Subscriber.query.filter_by(email=email).first()
    if existing_subscriber:
        return jsonify({"message": "Already subscribed"}), 200  # ✅ Prevent duplicate entries

    # Save subscriber
    new_subscriber = Subscriber(email=email)
    db.session.add(new_subscriber)
    db.session.commit()

    return jsonify({"message": "Subscription successful"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
