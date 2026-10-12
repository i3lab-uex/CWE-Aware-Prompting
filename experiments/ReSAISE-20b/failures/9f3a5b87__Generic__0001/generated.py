import json
import os
from typing import Dict, Optional

# Example trusted signatures (should be filled with real values)
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "config.json": "abc123def456",
    # Add more trusted signatures here
}

def handle_config_data(file_name: str, file_signature: str) -> Optional[Dict]:
    """
    Retrieve configuration data from a JSON file and verify its signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    file_signature : str
        Signature provided for this file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid;
        otherwise, ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Verify that the file exists
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Check the provided signature against the trusted list
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig is None or not _secure_compare(expected_sig, file_signature):
        # Signature mismatch
        return None

    # Read and parse the configuration file
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as exc:  # Catch JSON errors, file read errors, etc.
        # Log the exception if logging is available; here we just propagate
        raise IOError(f"Failed to read or parse configuration file '{file_name}': {exc}") from exc

    # Ensure the result is a dictionary
    if not isinstance(config, dict):
        raise ValueError(f"Configuration file '{file_name}' does not contain a JSON object")

    return config


def _secure_compare(a: str, b: str) -> bool:
    """
    Perform a timing‑attack resistant comparison of two strings.

    Parameters
    ----------
    a, b : str
        Strings to compare.

    Returns
    -------
    bool
        ``True`` if the strings are identical, otherwise ``False``.
    """
    try:
        # Python 3.5+ provides hmac.compare_digest
        import hmac
        return hmac.compare_digest(a, b)
    except Exception:
        # Fallback for very old Python versions (unlikely in modern code)
        return a == b