import os
import json
from datetime import datetime

REVOKED_KEYS_FILE = "revoked_keys.json"

def load_revoked_keys():
    if not os.path.exists(REVOKED_KEYS_FILE):
        return {}
    with open(REVOKED_KEYS_FILE, "r") as f:
        return json.load(f)

def save_revoked_keys(revoked_keys):
    with open(REVOKED_KEYS_FILE, "w") as f:
        json.dump(revoked_keys, f, indent=2)

def revoke_license(license_key, reason="Manually revoked"):
    revoked_keys = load_revoked_keys()

    if license_key in revoked_keys:
        print(f"⚠️ License '{license_key}' is already revoked.")
        return

    revoked_keys[license_key] = {
        "revoked_at": datetime.utcnow().isoformat() + "Z",
        "reason": reason
    }

    save_revoked_keys(revoked_keys)
    print(f"✅ License '{license_key}' has been revoked and logged.")

def main():
    license_key = input("🔑 Enter license key to revoke: ").strip()
    reason = input("✏️ Enter reason for revocation (optional): ").strip() or "Manually revoked"
    revoke_license(license_key, reason)

if __name__ == "__main__":
    main()
