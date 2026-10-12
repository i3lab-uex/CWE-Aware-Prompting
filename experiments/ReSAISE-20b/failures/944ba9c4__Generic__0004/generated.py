import json
import os
import hmac
from typing import Optional, Dict

# Example trusted signatures mapping.
# In real usage this should be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # 'config.json': 'sha256hashstring...',
}

def validate_config_file(filename: str, cryptographic_signature: str) -> Optional[Dict]:
    """
    Retrieve configuration data from a file and validate its cryptographic signature.

    Parameters
    ----------
    filename : str
        Name of the configuration file.
    cryptographic_signature : str
        Signature sent with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist.")

    # Retrieve the trusted signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_signature is None:
        # No trusted signature known for this file – treat as invalid
        return None

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(cryptographic_signature, expected_signature):
        return None

    # Read and parse the configuration file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers I/O errors; ValueError covers JSON parsing errors
        raise IOError(f"Failed to read or parse configuration file '{filename}': {exc}") from exc

    return data