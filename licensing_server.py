import os
import re
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

KEYGEN_ACCOUNT_ID = os.getenv("KEYGEN_ACCOUNT_ID")
KEYGEN_BASE_URL = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}"

def get_token_permissions(auth_token):
    url = f"{KEYGEN_BASE_URL}/me"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.api+json"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["meta"].get("permissions", [])
        else:
            return []
    except Exception:
        return []

def require_permission(token, required_scope):
    permissions = get_token_permissions(token)
    return required_scope in permissions

@app.route("/validate", methods=["POST"])
def validate_license():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split()[1]
    if not require_permission(token, "license.validate"):
        return jsonify({"error": "Insufficient permissions"}), 403

    if not request.json:
        return jsonify({"error": "JSON payload required"}), 400

    license_key = request.json.get("license_key")
    if not license_key:
        return jsonify({"error": "License key required"}), 400

    if not re.match(r'^[A-Z0-9]{6}(-[A-Z0-9]{6}){4}-V\d+$', license_key):
        return jsonify({"error": "Invalid license key format"}), 400

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json"
    }
    url = f"{KEYGEN_BASE_URL}/licenses/actions/validate-key"
    payload = {
        "meta": {
            "key": license_key
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return jsonify({"valid": True, "details": response.json()}), 200
        else:
            return jsonify({"valid": False, "error": response.json()}), 403
    except requests.exceptions.RequestException:
        return jsonify({"valid": False, "error": "Network error"}), 500

if __name__ == "__main__":
    app.run(port=5000)
