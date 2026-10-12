import json
import os
import hmac

# Global dictionary mapping config file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "a1b2c3d4e5f6g7h8i9j0",
    "db_config.json":  "1234567890abcdef1234",
    # Add more trusted signatures here
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        Name of the configuration file to load (relative to current working directory).
    signature : str
        Cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Verify that we have a trusted signature for this config
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if trusted_sig is None:
        # No known signature for this config – treat as untrusted
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # Resolve the absolute path to avoid directory traversal
    config_path = os.path.abspath(config_name)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_name}' not found.")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        # Re‑raise as IOError to conform with the spec
        raise IOError(f"Error reading configuration file '{config_name}': {exc}") from exc

    if not isinstance(data, dict):
        # Configuration must be a dictionary
        return None

    return data