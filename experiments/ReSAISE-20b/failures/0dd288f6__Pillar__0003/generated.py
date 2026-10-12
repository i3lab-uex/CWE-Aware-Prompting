import os
import json
import hashlib
import hmac

# Global dictionary mapping configuration filenames to their trusted SHA256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (the actual signatures should be filled in by the application)
    "app_config.json": "3b5d5c3712955042212316173ccf37be",
    # Add more configuration files and their corresponding signatures here
}

def apply_config_data(configuration_name: str, config_signature: str) -> dict | None:
    """
    Load and validate a configuration file.

    Parameters
    ----------
    configuration_name : str
        Name of the configuration file to load (relative path from current working directory).
    config_signature : str
        Expected cryptographic signature (hex string) of the configuration file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is verified;
        otherwise, None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Resolve absolute path to guard against directory traversal
    config_path = os.path.abspath(configuration_name)

    # Ensure the file exists and is a regular file
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Read the entire file in binary mode
    try:
        with open(config_path, "rb") as f:
            file_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}") from exc

    # Compute the SHA-256 digest of the file contents
    computed_digest = hashlib.sha256(file_bytes).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_digest, config_signature):
        # Signature mismatch – reject the configuration
        return None

    # Parse JSON content into a dictionary; handle potential decoding errors
    try:
        config_dict = json.loads(file_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        # If the file is not valid JSON, treat it as an invalid configuration
        return None

    # Optionally, verify that the signature matches the trusted one in the global dict
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_sig is not None and not hmac.compare_digest(expected_sig, config_signature):
        # The provided signature does not match the trusted one
        return None

    return config_dict