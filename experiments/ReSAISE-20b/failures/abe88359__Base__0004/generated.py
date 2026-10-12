import os
import json
import hmac

# Global dictionary mapping config filenames to their correct signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; replace with actual trusted values
    "app_config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    "db_config.json":  "6f1ed002ab5595859014ebf0951522d9",
}

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Reads a configuration file and verifies its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name (or relative path) of the configuration file.
    cfg_signature : str
        The cryptographic signature (hex string) provided for verification.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches.
        `None` if the signature does not match.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path and ensure the file exists
    cfg_path = os.path.abspath(cfg_name)
    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_name}' not found at {cfg_path}")

    # Read the raw bytes of the configuration file
    try:
        with open(cfg_path, "rb") as f:
            raw_data = f.read()
    except Exception as e:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{cfg_name}': {e}")

    # Compute the expected signature from the trusted store
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if not trusted_sig:
        # If we don't have a known signature, treat as untrusted
        return None

    # Compare signatures in constant time to avoid timing attacks
    if not hmac.compare_digest(cfg_signature.lower(), trusted_sig.lower()):
        return None

    # Parse the configuration content (assumed to be JSON)
    try:
        config = json.loads(raw_data.decode("utf-8"))
    except Exception as e:  # pragma: no cover
        raise IOError(f"Failed to parse configuration file '{cfg_name}': {e}")

    return config