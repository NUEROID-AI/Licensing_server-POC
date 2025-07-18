import json
import base64
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

# Load private key
try:
    with open("private_key.pem", "rb") as f:
        key = RSA.import_key(f.read())
except FileNotFoundError:
    print("❌ Error: private_key.pem not found")
    exit(1)
except Exception as e:
    print(f"❌ Error loading private key: {e}")
    exit(1)
# License payload (edit values if needed)
license_data = {
    "license_key": "add_license_key",
    "product_id": "add_product_id",
    "expiry": "add_expiry_date"  
}
# Validate required fields
required_fields = ["license_key", "product_id", "expiry"]
for field in required_fields:
    if not license_data.get(field):
        print(f"❌ Error: {field} is required")
        exit(1)

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
