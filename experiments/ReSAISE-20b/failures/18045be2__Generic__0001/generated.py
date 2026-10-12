import json
import os
import hmac

# Example trusted signatures mapping.
# In a real system these would be securely stored and managed.
TRUSTED_CONFIG_SIGNATURES = {
    # signature: config_file_name
    "a1b2c3d4e5f6g7h8i9j0": "app_config.json",
    "1234567890abcdef1234": "db_config.yaml",
}

# Base directory where configuration files are stored.
CONFIG_BASE_DIR = "/etc/myapp/config"


def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Load configuration data from a file after validating the provided
    cryptographic signature.

    Parameters
    ----------
    config_file : str
        Name of the configuration file to read.
    provided_signature : str
        Cryptographic signature that must match the trusted entry.

    Returns
    -------
    dict | None
        Parsed configuration data if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or opened.
    """
    # 1. Validate that the provided signature is trusted for this file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if not expected_file or expected_file != config_file:
        # Signature does not match the file.
        return None

    # 2. Construct absolute path and ensure it resides within the base directory
    safe_path = os.path.abspath(os.path.join(CONFIG_BASE_DIR, config_file))
    if not safe_path.startswith(os.path.abspath(CONFIG_BASE_DIR)):
        # Path traversal attempt detected
        return None

    try:
        with open(safe_path, "r", encoding="utf-8") as fp:
            content = fp.read()
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{config_file}' not found.") from exc

    # 3. Parse the configuration data.
    # Assume JSON for simplicity; adapt as needed.
    try:
        config_data = json.loads(content)
    except json.JSONDecodeError:
        # Invalid configuration format
        return None

    return config_data