import os
import hmac
import hashlib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# Shopify HMAC Secret
SHOPIFY_SHARED_SECRET = os.getenv("SHOPIFY_SHARED_SECRET")

# Model for storing subscribers
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

def verify_shopify_request(request):
    """ Validate Shopify webhook using HMAC signature """
    if not SHOPIFY_SHARED_SECRET:
        return False

    shopify_hmac = request.headers.get("X-Shopify-Hmac-Sha256")

    if not shopify_hmac:
        return False

    data = request.get_data()
    calculated_hmac = hmac.new(SHOPIFY_SHARED_SECRET.encode(), data, hashlib.sha256).digest()

    return hmac.compare_digest(shopify_hmac, calculated_hmac)

@app.route("/subscribe", methods=["POST"])
@limiter.limit("5 per minute")  # ⏳ Limit to 5 requests per minute
def subscribe():

    """ Handle newsletter subscriptions securely """
    # if not verify_shopify_request(request):
    #     return jsonify({"error": "Unauthorized request"}), 403  # 🚨 Reject invalid requests

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
