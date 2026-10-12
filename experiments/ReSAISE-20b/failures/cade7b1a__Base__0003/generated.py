import json
import os

# Global dictionary that maps configuration file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries: the signature strings should be computed
    # using a secure method (e.g., HMAC or RSA) in production.
    "app_config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    "db_config.json":  "e99a18c428cb38d5f260853678922e03",
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Args:
        config_name: The name of the configuration JSON file to load.
        signature:   The cryptographic signature that accompanies the data.

    Returns:
        The configuration data as a dictionary if the signature matches
        the trusted value; otherwise, None.

    Raises:
        IOError: If the configuration file cannot be found.
    """
    # Ensure we have a trusted signature for this config
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if expected_sig is None:
        # No trusted signature known; treat as untrusted.
        return None

    # Verify the provided signature matches the trusted one
    if signature != expected_sig:
        return None

    # Attempt to load the configuration file
    try:
        with open(config_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{config_name}' not found") from exc

    # Basic type check to ensure data is a dictionary
    if not isinstance(data, dict):
        return None

    return data