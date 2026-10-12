import hashlib
import os
from typing import Dict, Optional

# Example trusted signatures dictionary (to be populated elsewhere)
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config.json": "a3b1c2d4e5f6..."
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA-256 hex digest of a file's contents.
    """
    hash_obj = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    sign : str
        Cryptographic signature supplied by the caller (hex string).

    Returns
    -------
    dict or None
        Parsed configuration dictionary if the signature is valid.
        ``None`` if the supplied signature does not match the file
        or the trusted signature.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path and ensure file exists
    try:
        abs_path = os.path.abspath(file_name)
        if not os.path.isfile(abs_path):
            raise IOError(f"Configuration file '{file_name}' not found.")
    except OSError as exc:
        raise IOError(f"Error accessing configuration file '{file_name}': {exc}") from exc

    # Compute the actual signature of the file
    try:
        actual_sig = _compute_file_signature(abs_path)
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc

    # Verify supplied signature matches the actual signature
    if not hashlib.compare_digest(sign.lower(), actual_sig.lower()):
        return None

    # Verify the signature against the trusted list
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if not trusted_sig or not hashlib.compare_digest(trusted_sig.lower(), actual_sig.lower()):
        return None

    # Load the configuration (assuming JSON format for illustration)
    try:
        import json
        with open(abs_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as exc:  # Catch broad errors for malformed JSON, etc.
        raise IOError(f"Failed to parse configuration file '{file_name}': {exc}") from exc

    return config