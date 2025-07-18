#!/usr/bin/env python3
import json
import os
import sys
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

LICENSE_FILE = "signed_license.json"
PUBLIC_KEY_FILE = "public_key.pem"

def load_signed_license():
    try:
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ License file not found. Ensure 'signed_license.json' is present.")
        sys.exit(1)

def verify_signature(license_data, signature_hex):
    try:
        license_json = json.dumps(license_data, separators=(',', ':'), sort_keys=True).encode("utf-8")
        h = SHA256.new(license_json)

        with open(PUBLIC_KEY_FILE, "r") as f:
            pubkey = RSA.import_key(f.read())

        pkcs1_15.new(pubkey).verify(h, bytes.fromhex(signature_hex))
        return True
    except (ValueError, TypeError):
        return False

def main():
    print("🚀 Starting Roslab installation...")

    license = load_signed_license()
    license_data = license.get("license")
    signature = license.get("signature")

    if not license_data or not signature:
        print("❌ Invalid license structure.")
        sys.exit(1)

    if verify_signature(license_data, signature):
        print("✅ License is valid. Proceeding with installation...")
        print("📦 Installing Roslab components...")
        # Mock install step
        print("🎉 Installation completed successfully!")
    else:
        print("❌ License verification failed. Installation aborted.")
        sys.exit(1)

if __name__ == "__main__":
    main()
