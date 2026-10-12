import json
import hashlib
import os

# Example trusted signatures mapping (filename -> hex SHA256 hash)
TRUSTED_CONFIG_SIGNATURES = {
    # 'config.json': 'e3b0c442...'
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve and validate configuration data from a file.

    Parameters
    ----------
    config_filename : str
        Path to the configuration file.
    crypt_signature : str
        Expected SHA256 hex digest of the file's contents.

    Returns
    -------
    dict or None
        Parsed configuration dictionary if signature matches, otherwise None.

    Raises
    ------
    IOError
        If the file does not exist.
    """
    # Ensure the file exists; raise a descriptive IOError if it doesn't
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Read the raw bytes of the file
    with open(config_filename, "rb") as f:
        data_bytes = f.read()

    # Compute SHA256 digest of the file contents
    computed_digest = hashlib.sha256(data_bytes).hexdigest()

    # Validate against the expected signature
    if computed_digest.lower() != crypt_signature.lower():
        return None

    # Safely parse JSON; if invalid, return None
    try:
        config_text = data_bytes.decode("utf-8")
        config_dict = json.loads(config_text)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None

    # Optionally check that the config filename matches a trusted entry
    if config_filename not in TRUSTED_CONFIG_SIGNATURES:
        return None

    # Final check: ensure the stored signature matches computed digest
    if TRUSTED_CONFIG_SIGNATURES[config_filename].lower() != computed_digest.lower():
        return None

    return config_dict