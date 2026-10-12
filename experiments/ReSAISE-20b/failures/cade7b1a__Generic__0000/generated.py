import json
import os

# Global dictionary mapping configuration file names to trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (populate with real values as needed)
    "app_config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    "db_config.json": "e99a18c428cb38d5f260853678922e03",
}


def process_config_data(config_name: str, signature: str):
    """
    Load configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load.
    signature : str
        The cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found.
    """
    # Resolve the absolute path to guard against relative path traversal
    config_path = os.path.abspath(config_name)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Read the configuration data
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            # If the file is not valid JSON, treat it as invalid
            return None

    # Verify signature against the trusted value
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if trusted_sig is None:
        # No trusted signature available for this config
        return None

    if signature != trusted_sig:
        # Signature mismatch; do not expose configuration data
        return None

    return config_data