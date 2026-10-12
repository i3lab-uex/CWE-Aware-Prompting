import json
import os
import hmac

# Example trusted signatures dictionary (filename -> hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "config.yaml": "a1b2c3d4e5f6...",
    # Add more trusted signatures here
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from `filename` and verify that the provided
    cryptographic signature matches the trusted one.

    Parameters:
        filename (str): Path to the configuration file.
        cryptographic_signature (str): Signature sent with the config data.

    Returns:
        dict: Parsed configuration data if signature is valid.
        None: If the signature does not match.

    Raises:
        IOError: If `filename` does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Load the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # No trusted signature known for this file
        return None

    # Verify the provided signature against the expected one using a timing‑safe comparison
    if not hmac.compare_digest(cryptographic_signature, expected_sig):
        return None

    # Read and parse the configuration file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # Assuming JSON format for simplicity; adjust if needed
            config_data = json.load(f)
    except Exception as exc:
        # Re‑raise as IOError to match the contract
        raise IOError(f"Failed to read configuration file '{filename}': {exc}") from exc

    return config_data