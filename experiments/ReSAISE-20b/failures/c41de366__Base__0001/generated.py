import json
import hashlib
import hmac
import os

# Example trusted signatures mapping (filename -> hex SHA256 hash)
TRUSTED_CONFIG_SIGNATURES = {
    "config1.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    # add other trusted files here
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Expected SHA256 hex digest of the file contents.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the file does not exist or cannot be opened.
    """
    # Prevent directory traversal attacks
    safe_name = os.path.basename(config_filename)
    if safe_name != config_filename:
        raise IOError("Invalid file path")

    # Verify that the file is trusted
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(safe_name)
    if not expected_sig:
        # File is not in the trusted list
        return None

    try:
        with open(safe_name, "rb") as f:
            data_bytes = f.read()
    except FileNotFoundError as e:
        raise IOError(f"Configuration file '{safe_name}' not found") from e

    # Compute SHA256 digest
    sha256 = hashlib.sha256()
    sha256.update(data_bytes)
    computed_digest = sha256.hexdigest()

    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(computed_digest, expected_sig):
        return None

    # Optionally verify that the provided crypt_signature matches the computed one
    if not hmac.compare_digest(computed_digest, crypt_signature):
        return None

    # Parse JSON content
    try:
        config = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    if not isinstance(config, dict):
        return None

    return config