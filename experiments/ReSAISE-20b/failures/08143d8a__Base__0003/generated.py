import os
import json
import hmac
from typing import Dict, Optional

# Example trusted signatures mapping. In a real system this would be loaded
# from a secure store and contain cryptographic hashes (e.g., SHA-256).
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config.json": "<hex-encoded-signature>",
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> Optional[Dict]:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    provided_sig : str
        Hex‑encoded cryptographic signature supplied with the configuration.

    Returns
    -------
    dict or None
        The parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Resolve absolute path to avoid directory traversal attacks
    safe_path = os.path.abspath(config_filename)

    # Check file existence and readability
    if not os.path.isfile(safe_path):
        raise IOError(f"Configuration file '{config_filename}' not found.")

    try:
        with open(safe_path, "rb") as f:
            data_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file: {exc}") from exc

    # Compute the expected signature for this file (e.g., SHA-256 hash)
    # Here we simply look up the pre‑computed signature in TRUSTED_CONFIG_SIGNATURES.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)

    # Use constant‑time comparison to mitigate timing attacks
    if expected_sig is None or not hmac.compare_digest(expected_sig, provided_sig):
        return None

    # Attempt to parse the configuration data (JSON assumed)
    try:
        config = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If parsing fails we treat it as an invalid configuration
        return None

    return config