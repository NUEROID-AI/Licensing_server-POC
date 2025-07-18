import os
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

KEYGEN_ACCOUNT_ID = os.getenv("KEYGEN_ACCOUNT_ID")
KEYGEN_PRODUCT_ID = os.getenv("KEYGEN_PRODUCT_ID")
KEYGEN_API_TOKEN = os.getenv("KEYGEN_API_TOKEN")

KEYGEN_BASE_URL = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}"

@app.route("/validate", methods=["POST"])
def validate_license():
    if not request.json:
        return jsonify({"error": "JSON payload required"}), 400

    license_key = request.json.get("license_key")
    if not license_key:
        return jsonify({"error": "License key required"}), 400

    # Basic license key format validation
    if not re.match(r'^[A-Z0-9]{6}(-[A-Z0-9]{6}){5}-V\d+$', license_key):
        return jsonify({"error": "Invalid license key format"}), 400

    url = f"{KEYGEN_BASE_URL}/licenses/actions/validate-key"
    headers = {
        "Authorization": f"Bearer {KEYGEN_API_TOKEN}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json"
    }
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
            try:
                error_data = response.json()
            except ValueError:
                error_data = {"message": "Invalid JSON response from Keygen"}
            return jsonify({"valid": False, "error": error_data}), 403

    except requests.exceptions.RequestException as e:
        return jsonify({"valid": False, "error": f"Network error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000)
