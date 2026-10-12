import os
import json
import hashlib
from hmac import compare_digest

# Example trusted signatures mapping (filename -> expected SHA256 hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "d2c6f8b3e9a4a1b5c7e8f2d0e6a1b3c9f4d2e7c5b8a9f0c6d1e3b5a7c9d2f4b",
    # Add more trusted file signatures here
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA256 hex digest of the file contents.
    """
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from `file_name` and verify its cryptographic
    signature against the trusted signatures mapping. If the file does not
    exist, an IOError is raised.

    Parameters:
        file_name (str): Name of the configuration file.
        file_signature (str): Signature sent with the data (hex string).

    Returns:
        dict | None: The parsed JSON configuration if signature is valid,
                     otherwise None.
    """
    # Resolve absolute path to avoid directory traversal issues
    safe_path = os.path.abspath(file_name)

    # Ensure the file is within a trusted directory (if needed)
    # For this example we simply check existence
    if not os.path.isfile(safe_path):
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Compute the actual signature of the file
    try:
        computed_sig = _compute_file_signature(safe_path)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read or compute signature for '{file_name}': {exc}")

    # Retrieve the expected signature from the trusted list
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)

    # If no entry exists for this file, treat as untrusted
    if expected_sig is None:
        return None

    # Compare signatures using constant‑time comparison to mitigate timing attacks
    if not compare_digest(computed_sig, expected_sig):
        return None

    # Compare with the signature supplied by the caller (optional but double‑check)
    if not compare_digest(computed_sig, file_signature):
        return None

    # Load and return the configuration data
    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:  # pragma: no cover
        raise IOError(f"Failed to parse configuration file '{file_name}': {exc}")

    return config