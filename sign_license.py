# sign_license.py
import os
import json
import requests
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

load_dotenv()

KEYGEN_ACCOUNT_ID = os.getenv("KEYGEN_ACCOUNT_ID")
KEYGEN_API_TOKEN = os.getenv("KEYGEN_API_TOKEN")
PRIVATE_KEY_PATH = "private_key.pem"
SIGNED_JSON_PATH = "signed_license.json"

def fetch_license_data(license_key):
    url = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}/licenses/actions/validate-key"
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

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("❌ Error: License validation failed")
        print(response.json())
        exit(1)

    return response.json()["meta"]

def sign_data(data, private_key_path):
    message = json.dumps(data, separators=(",", ":"), sort_keys=True).encode()
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()

def main():
    license_key = input("🔑 Enter license key to sign: ").strip()

    # Full response (needed for attributes like expiry)
    url = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}/licenses/actions/validate-key"
    headers = {
        "Authorization": f"Bearer {KEYGEN_API_TOKEN}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json"
    }
    payload = { "meta": { "key": license_key } }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("❌ Error: License validation failed")
        print(response.json())
        exit(1)

    meta = response.json()["meta"]
    attributes = response.json()["data"]["attributes"]

    # Merge meta and attributes into one payload
    license_data = {
        **meta,
        "key": license_key,
        "name": attributes.get("name", "Unknown"),
        "expires_at": attributes.get("expiry", "N/A"),
        "starts_at": attributes.get("starts", "N/A")
    }

    signature = sign_data(license_data, PRIVATE_KEY_PATH)

    signed_blob = {
        "data": license_data,
        "signature": signature
    }

    with open(SIGNED_JSON_PATH, "w") as f:
        json.dump(signed_blob, f, indent=2)

    print("✅ signed_license.json created and signed.")

if __name__ == "__main__":
    main()
