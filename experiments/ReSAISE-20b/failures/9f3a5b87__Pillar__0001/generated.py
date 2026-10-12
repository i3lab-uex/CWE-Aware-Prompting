import json
import hashlib
import hmac
from pathlib import Path

# Global dictionary containing the expected signature for each trusted file.
# Example: {"config.json": "a1b2c3d4..."}
TRUSTED_CONFIG_SIGNATURES = {
    # Populate with real signatures as needed
}

def _compute_signature(data: bytes) -> str:
    """
    Compute a SHA256 HMAC signature of the given data using a secret key.
    The secret key should be stored securely (e.g., environment variable or
    hardware security module). For this example, we use a hard‑coded key,
    but in production replace it with an appropriate secure source.
    """
    # WARNING: In real deployments, never hard‑code secret keys.
    secret_key = b"super_secret_key"
    return hmac.new(secret_key, data, hashlib.sha256).hexdigest()

def handle_config_data(file_name: str, file_signature: str) -> dict | None:
    """
    Retrieve configuration data from *file_name*, verify its cryptographic
    signature against the expected value in TRUSTED_CONFIG_SIGNATURES, and
    return the parsed JSON dictionary if valid. Otherwise return None.
    
    Raises:
        IOError: If *file_name* does not exist or is unreadable.
    """
    file_path = Path(file_name)

    # 1. Check that the file exists and is readable
    if not file_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist or is inaccessible.")

    # 2. Read the raw bytes of the file
    try:
        data = file_path.read_bytes()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc

    # 3. Compute the expected signature for this data
    computed_sig = _compute_signature(data)

    # 4. Retrieve the trusted signature for this file (if any)
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)

    # 5. Verify that the provided signature matches the computed one
    if expected_sig is None:
        # No trusted signature registered for this file; treat as invalid
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_sig, expected_sig):
        return None

    # 6. Verify that the provided signature matches the one supplied by caller
    if not hmac.compare_digest(file_signature, computed_sig):
        return None

    # 7. Parse JSON content safely
    try:
        config = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed JSON or encoding issues
        return None

    if not isinstance(config, dict):
        # Expect a dictionary; reject other structures
        return None

    return config