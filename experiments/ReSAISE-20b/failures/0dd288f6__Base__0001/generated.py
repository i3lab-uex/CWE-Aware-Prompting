import os
import hashlib
import hmac

# Global dictionary mapping configuration file names to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # 'app_config.json': '3a7bd3e2360a... (64 hex chars)',
    # Add your own trusted signatures here.
}

def _compute_file_signature(filepath: str) -> bytes:
    """
    Compute the SHA‑256 digest of a file in a memory‑efficient way.
    Returns the digest as bytes.
    """
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.digest()

def apply_config_data(configuration_name: str, config_signature: str):
    """
    Reads a configuration file and verifies its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The filename of the configuration to load.
    config_signature : str
        The expected hexadecimal SHA‑256 signature string.

    Returns
    -------
    dict or None
        Parsed configuration data as a dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path and ensure the file exists
    config_path = os.path.abspath(configuration_name)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Compute the actual signature of the file
    try:
        actual_sig_bytes = _compute_file_signature(config_path)
    except Exception as exc:
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}") from exc

    # Convert expected signature (hex string) to bytes
    try:
        expected_sig_bytes = bytes.fromhex(config_signature)
    except ValueError as exc:
        raise ValueError(f"Invalid signature format for '{configuration_name}': {exc}") from exc

    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(actual_sig_bytes, expected_sig_bytes):
        # Signature mismatch; do not load the configuration
        return None

    # Signature verified – read and parse the configuration (assumed JSON)
    import json
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as exc:
        raise IOError(f"Failed to parse configuration file '{configuration_name}': {exc}") from exc

    return config_data