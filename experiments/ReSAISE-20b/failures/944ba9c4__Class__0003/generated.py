import json
from pathlib import Path
import hmac

# Global dictionary mapping filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    # "settings.yaml": "e99a18c428cb38d5f260853678922e03",
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from `filename` and verify that the
    supplied cryptographic signature matches the trusted signature for
    this file.

    Parameters
    ----------
    filename : str
        Name of the configuration file.
    cryptographic_signature : str
        Signature that was sent alongside the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If `filename` does not exist.
    """
    file_path = Path(filename)

    # Check existence and raise IOError if missing
    if not file_path.is_file():
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Retrieve the trusted signature for this file
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if trusted_sig is None:
        # No known signature for this file – treat as invalid
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(cryptographic_signature, trusted_sig):
        return None

    # Read and parse the file safely
    try:
        with file_path.open("r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, ValueError) as e:
        # If file cannot be read or JSON is malformed, treat as invalid
        return None

    if not isinstance(config_data, dict):
        # Expecting a dictionary; otherwise treat as invalid
        return None

    return config_data