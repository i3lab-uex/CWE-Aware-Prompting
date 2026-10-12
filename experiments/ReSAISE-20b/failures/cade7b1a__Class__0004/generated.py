import os
import json
import hmac
from typing import Dict, Optional

# Global dictionary mapping config file names to their trusted cryptographic signatures.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be populated from a secure source.
    "app_config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbddc7b2c4e5f8c5c1f3a",
    "db_config.json":  "6b86b273ff34fce19d6b804eff5a3e4089c7bd2a9c8f4e9d6b1e5b0e2f3a7c9d",
}

def _secure_compare(a: str, b: str) -> bool:
    """
    Constant-time comparison of two strings to prevent timing attacks.
    """
    return hmac.compare_digest(a.encode(), b.encode())

def process_config_data(config_name: str, signature: str) -> Optional[Dict]:
    """
    Load a JSON configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load.
    signature : str
        The cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict or None
        The parsed JSON configuration if the signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path (prevent directory traversal by ensuring the name contains no slashes)
    if os.path.sep in config_name or ".." in config_name:
        raise IOError(f"Invalid configuration name: {config_name!r}")

    # Construct the file path relative to a trusted directory
    config_dir = os.path.join(os.getcwd(), "trusted_configs")
    file_path = os.path.join(config_dir, config_name)

    # Attempt to read the file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise IOError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError as e:
        # If JSON is malformed, treat it as invalid data
        print(f"Error decoding JSON from {file_path}: {e}")
        return None

    # Verify the signature against the trusted list
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if expected_sig is None:
        # No trusted signature known for this file
        print(f"No trusted signature found for {config_name}")
        return None

    if not _secure_compare(signature, expected_sig):
        # Signature mismatch
        print(f"Signature verification failed for {config_name}")
        return None

    # Signature matches; return the configuration data
    return data