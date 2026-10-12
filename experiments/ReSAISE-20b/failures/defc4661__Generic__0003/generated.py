import json
import os
import hmac
from typing import Dict, Optional

# Example global dictionary containing the correct signatures for each file.
# In a real application this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # example SHA-256
    # add more entries as needed...
}


def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    sign : str
        The cryptographic signature (hex string) claimed for the file.

    Returns
    -------
    dict or None
        Parsed configuration dictionary if signature is verified, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path for safety
    config_path = os.path.abspath(file_name)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{file_name}' not found")

    # Compute SHA-256 hash of the file contents
    try:
        with open(config_path, "rb") as f:
            data = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{file_name}': {exc}") from exc

    # Compute hash
    import hashlib
    computed_hash = hashlib.sha256(data).hexdigest()

    # Retrieve the trusted signature for this file
    trusted_sign = TRUSTED_CONFIG_SIGNATURES.get(file_name)

    # If there is no trusted signature defined, consider it invalid
    if not trusted_sign:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_hash, trusted_sign):
        return None

    # Parse the configuration (assuming JSON format)
    try:
        config = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If parsing fails we treat it as an invalid configuration
        return None

    if not isinstance(config, dict):
        # Ensure the top‑level object is a dictionary
        return None

    return config