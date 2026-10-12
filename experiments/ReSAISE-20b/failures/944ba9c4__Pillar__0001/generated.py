import json
from pathlib import Path
from typing import Dict, Optional

# Trusted signatures for configuration files.
# In a real system this would be securely stored (e.g., in an HSM or
# retrieved from a trusted remote service).  For demonstration we use a
# simple in‑memory dictionary.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example:
    # "config.yaml": "abcdef1234567890",
}

def validate_config_file(
    filename: str,
    cryptographic_signature: str
) -> Optional[Dict]:
    """
    Load configuration data from *filename* and verify that the supplied
    *cryptographic_signature* matches the trusted signature for that file.

    Parameters
    ----------
    filename : str
        Path to the configuration file.
    cryptographic_signature : str
        Signature provided by the caller (e.g., from a remote server).

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid; otherwise `None`.

    Raises
    ------
    IOError
        If *filename* does not exist or cannot be read.
    """
    path = Path(filename)

    # Ensure the file exists and is readable
    if not path.is_file():
        raise IOError(f"Configuration file '{filename}' does not exist.")

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # If we have no record of the file, treat it as invalid
        return None

    # Verify the supplied signature matches the trusted one.
    # Use a constant‑time comparison to mitigate timing attacks.
    if not _constant_time_compare(cryptographic_signature, expected_sig):
        return None

    # Read and parse the configuration file
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        # Propagate file I/O errors; decoding errors are treated as
        # invalid configuration data.
        raise IOError(f"Failed to read or parse '{filename}': {exc}") from exc

    return data


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to avoid timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0