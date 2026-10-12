import json
import os
import hmac
from typing import Dict, Optional

# Global mapping of configuration file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real signatures.
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "db_config.json":  "5d41402abc4b2a76b9719d911017c592",
}

def process_config_data(config_name: str, signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The filename of the configuration to load.
    signature : str
        The cryptographic signature accompanying the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path – only allow files in the current working directory
    # to prevent arbitrary file access.
    config_path = os.path.abspath(config_name)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Read the raw bytes of the configuration to verify against the signature.
    try:
        with open(config_path, "rb") as f:
            data_bytes = f.read()
    except OSError as exc:  # pragma: no cover
        raise IOError(f"Error reading configuration file '{config_name}': {exc}") from exc

    # The trusted signature for this config must exist.
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not trusted_sig:
        # No known signature for this file – treat as untrusted.
        return None

    # Use constant‑time comparison to avoid timing attacks (CWE-345 mitigation).
    if not hmac.compare_digest(signature, trusted_sig):
        # Signature mismatch – reject the configuration.
        return None

    # Parse JSON safely. If parsing fails, treat as invalid data.
    try:
        config_dict = json.loads(data_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):  # pragma: no cover
        return None

    if not isinstance(config_dict, dict):
        # Unexpected structure – reject.
        return None

    return config_dict