import json
import os
import hmac
from typing import Dict, Optional

# Global dictionary mapping configuration filenames to their expected signatures.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real values
    "app_config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    "db_config.json": "e99a18c428cb38d5f260853678922e03",
}


def verify_configuration_file(cfg_name: str, cfg_signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature against the
    trusted signatures list.

    Parameters:
        cfg_name (str): The filename of the configuration file.
        cfg_signature (str): The signature supplied for verification.

    Returns:
        dict: Parsed configuration data if the signature is verified.
        None: If the supplied signature does not match the trusted value.

    Raises:
        IOError: If the configuration file cannot be found or read.
    """
    # Resolve absolute path and ensure file exists
    config_path = os.path.abspath(cfg_name)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{cfg_name}' not found at {config_path}")

    # Retrieve the trusted signature for this configuration
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if expected_sig is None:
        # If we don't have a trusted signature for this file, consider it untrusted
        return None

    # Use constant‑time comparison to avoid timing attacks (CWE‑347)
    if not hmac.compare_digest(cfg_signature, expected_sig):
        return None

    # Load and parse the configuration file (assumed to be JSON)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{cfg_name}': {exc}") from exc