import json
import base64
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

# Load private key
with open("private_key.pem", "rb") as f:
    key = RSA.import_key(f.read())

# License payload (edit values if needed)
license_data = {
    "license_key": "A03B74-BD87CA-9DFBB9-2E9F0D-16FA9E-V3",
    "product_id": "2d910f66-aa73-4030-9fab-4ac3a9450d3c",
    "expiry": "2026-07-01"
}

# Serialize (with sort + compact separators)
license_json = json.dumps(license_data, separators=(',', ':'), sort_keys=True).encode("utf-8")
h = SHA256.new(license_json)

# Sign it
signature = pkcs1_15.new(key).sign(h)

# Save signed license
signed_license = {
    "license": license_data,
    "signature": signature.hex()
}

with open("signed_license.json", "w") as f:
    json.dump(signed_license, f, indent=2)

print("✅ License signed and saved to signed_license.json")
