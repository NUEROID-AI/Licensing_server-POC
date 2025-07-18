# licensing_server.py

import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

KEYGEN_ACCOUNT_ID = os.getenv("KEYGEN_ACCOUNT_ID")
KEYGEN_PRODUCT_ID = os.getenv("KEYGEN_PRODUCT_ID")
KEYGEN_API_TOKEN = os.getenv("KEYGEN_API_TOKEN")

KEYGEN_BASE_URL = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}"

@app.route("/validate", methods=["POST"])
def validate_license():
    license_key = request.json.get("license_key")
    if not license_key:
        return jsonify({"error": "License key required"}), 400

    # Call Keygen API
    url = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}/licenses/actions/validate-key"
    headers = {
    "Authorization": f"Bearer {KEYGEN_API_TOKEN}",
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json"
}
    
    # Try simpler payload first
    payload = {
        "meta": {
            "key": license_key
        }
    }

    print("=== DEBUG URL ===")
    print(url)
    print("=== DEBUG HEADERS ===")
    print(headers)
    print("=== DEBUG PAYLOAD ===")
    print(payload)

    response = requests.post(url, headers=headers, json=payload)

    print("=== DEBUG RESPONSE ===")
    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        return jsonify({"valid": True, "details": response.json()}), 200
    else:
        return jsonify({"valid": False, "error": response.json()}), 403

if __name__ == "__main__":
    app.run(port=5000, debug=True)
