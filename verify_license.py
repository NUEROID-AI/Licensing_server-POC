import json
import sys
from datetime import datetime
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

def load_signed_license(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ License file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in license file: {path}")
        sys.exit(1)

def verify_license(signed_license):
    try:
        license_data = signed_license["license"]
        signature = bytes.fromhex(signed_license["signature"])
    except (KeyError, ValueError):
        print("❌ Invalid license format.")
        sys.exit(1)

    # ⏳ Expiry check (before signature validation)
    expiry = license_data.get("expiry")
    if not expiry:
        print("❌ License expiry date missing.")
        sys.exit(1)

    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
        if expiry_date < datetime.now():
            print("❌ License has expired.")
            sys.exit(1)
    except ValueError:
        print("❌ Invalid expiry date format. Expected YYYY-MM-DD.")
        sys.exit(1)

    # ❌ Revocation Check (offline simulation)
    if license_data.get("revoked", False):
       print("❌ License has been revoked.")
       sys.exit(1)

    # ✅ Signature verification
    license_json = json.dumps(license_data, separators=(',', ':'), sort_keys=True).encode("utf-8")
    h = SHA256.new(license_json)

    with open("public_key.pem", "r") as f:
        pubkey = RSA.import_key(f.read())

    try:
        pkcs1_15.new(pubkey).verify(h, signature)
        print("✅ Signature is valid. License verified.")
    except (ValueError, TypeError):
        print("❌ Signature is invalid. License is not valid.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_license.py <signed_license.json>")
        sys.exit(1)

    verify_license(load_signed_license(sys.argv[1]))
