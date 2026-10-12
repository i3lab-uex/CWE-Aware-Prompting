import os
import json
import hmac

# Global mapping of configuration file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (replace with real values in production)
    "app_config.json": "a1b2c3d4e5f6g7h8i9j0",
    "db_config.json":  "1234567890abcdef1234"
}


def process_config_data(config_name: str, signature: str):
    """
    Load configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        Name of the configuration file to load.
    signature : str
        Cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path for security (prevent directory traversal)
    config_path = os.path.abspath(config_name)

    # Ensure the file is within an allowed directory (example: ./configs)
    allowed_dir = os.path.abspath("./configs")
    if not config_path.startswith(allowed_dir):
        raise IOError(f"Access to {config_name} is forbidden.")

    # Read file contents
    try:
        with open(config_path, "rb") as f:
            data_bytes = f.read()
    except FileNotFoundError as e:
        raise IOError(f"Configuration file '{config_name}' not found.") from e

    # Compute the expected signature
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not expected_sig:
        # No trusted signature known for this file
        return None

    # Compare signatures securely to avoid timing attacks
    if not hmac.compare_digest(signature, expected_sig):
        return None

    # Parse JSON content into a dictionary
    try:
        config_dict = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Invalid JSON format
        return None

    return config_dict