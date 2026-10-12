import os
import json
import hmac

# Global trusted signatures dictionary.
# Example: {'config.json': 'a1b2c3d4...'}
TRUSTED_CONFIG_SIGNATURES = {
    # Populate with actual filenames and their expected signatures
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Validate a configuration file by checking its cryptographic signature
    against a trusted list.

    Args:
        filename (str): Path to the configuration file.
        cryptographic_signature (str): Signature sent with the config data.

    Returns:
        dict | None: Parsed configuration dictionary if signature is valid,
                     otherwise None.

    Raises:
        IOError: If the file does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Read the file contents safely
    try:
        with open(filename, "rb") as f:
            data_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{filename}': {exc}") from exc

    # Get the trusted signature for this file, if any
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # If no trusted signature exists, treat as invalid
        return None

    # Compare signatures using constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(expected_sig, cryptographic_signature):
        return None

    # Parse JSON safely
    try:
        config = json.loads(data_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Malformed file; treat as invalid
        return None

    # Ensure the parsed data is a dictionary
    if not isinstance(config, dict):
        return None

    return config