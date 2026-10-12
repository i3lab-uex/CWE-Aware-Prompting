import hashlib
import json
import os
from typing import Dict, Optional

# Example global dictionary mapping file names to their correct signatures.
# In a real system this would be populated from a trusted source.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config.json": "a1b2c3d4e5f6...",
}

def _compute_signature(data: bytes) -> str:
    """Return the SHA-256 hex digest of *data*."""
    return hashlib.sha256(data).hexdigest()

def _constant_time_compare(a: str, b: str) -> bool:
    """Compare two strings in constant time to mitigate timing attacks."""
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0

def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Read a configuration file, verify its signature and return the parsed
    configuration as a dictionary.

    Parameters:
        file_name: Name of the configuration file to read.
        sign: Expected cryptographic signature (hex string) for the file.

    Returns:
        The configuration dictionary if the signature is valid, otherwise None.

    Raises:
        IOError: If the file cannot be found or read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' not found")

    try:
        with open(file_name, "rb") as f:
            data = f.read()
    except OSError as exc:  # Handles permission errors, etc.
        raise IOError(f"Unable to read configuration file '{file_name}': {exc}") from exc

    # Compute the signature of the data
    computed_sig = _compute_signature(data)

    # Validate against the expected signature from TRUSTED_CONFIG_SIGNATURES
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig is None:
        # No known signature for this file – treat as untrusted
        return None

    if not _constant_time_compare(computed_sig, expected_sig):
        # Signature mismatch
        return None

    # Parse JSON content into a dictionary
    try:
        config = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Malformed content – treat as invalid
        return None

    if not isinstance(config, dict):
        # Configuration must be a JSON object
        return None

    return config