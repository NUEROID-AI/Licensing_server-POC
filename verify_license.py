# verify.py
import json
import base64
import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def verify_signature(data, signature_b64, public_key_path):
    try:
        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        # Canonicalize the actual data (rebuild the string)
        canonical_str = json.dumps(data, separators=(",", ":"), sort_keys=True).encode()
        signature = base64.b64decode(signature_b64)

        public_key.verify(
            signature,
            canonical_str,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"❌ Signature verification failed: {e}")
        return False

def print_license_info(data):
    print("\n✅ License is VALID. Here are the details:")
    print("--------------------------------------------------")
    print(f"🔑 License Key   : {data.get('key', 'N/A')}")
    print(f"👤 Client Name   : {data.get('user', {}).get('name', 'Unknown')}")
    print(f"📆 Start Date    : {data.get('starts_at', 'N/A')}")
    print(f"📅 Expiry Date   : {data.get('expires_at', 'N/A')}")
    print(f"🧾 Validity Code : {data.get('code', 'N/A')}")
    print(f"📌 Status Detail : {data.get('detail', 'N/A')}")
    print("--------------------------------------------------\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verify.py <signed_file.json>")
        return

    filename = sys.argv[1]

    try:
        with open(filename) as f:
            signed = json.load(f)
        data = signed["data"]
        signature = signed["signature"]
    except Exception as e:
        print(f"❌ Invalid format or file error: {e}")
        return

    if verify_signature(data, signature, "public_key.pem"):
        print("🔐 Signature is valid. License verified.")
        if data.get("valid") is True:
            print_license_info(data)
        else:
            print("⚠️ License is NOT valid.")
    else:
        print("❌ Invalid license signature.")

if __name__ == "__main__":
    main()
