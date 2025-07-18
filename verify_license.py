import json
import sys
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

def load_signed_license(path):
    with open(path, "r") as f:
        return json.load(f)

def verify_license(signed_license):
    try:
        license_data = signed_license["license"]
        signature = bytes.fromhex(signed_license["signature"])
    except (KeyError, ValueError):
        print("❌ Invalid license format.")
        sys.exit(1)

    license_json = json.dumps(license_data, separators=(',', ':'), sort_keys=True).encode("utf-8")
    h = SHA256.new(license_json)

    with open("public_key.pem", "r") as f:
        pubkey = RSA.import_key(f.read())

    try:
        pkcs1_15.new(pubkey).verify(h, signature)
        print("✅ Signature is valid. License verified.")
    except (ValueError, TypeError):
        print("❌ Signature is invalid. License is not valid.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_license.py <signed_license.json>")
        sys.exit(1)

    verify_license(load_signed_license(sys.argv[1]))
