import json
import os
import hmac
from typing import Dict, Optional

# Global mapping of trusted signatures to configuration file names.
# Example: {"abc123": "config.json", ...}
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Populate with real trusted signatures in production
}

def _signature_matches(sig: str, filename: str) -> bool:
    """
    Verify that the provided signature corresponds to the expected
    signature for *filename* in a constant‑time manner.
    """
    expected = TRUSTED_CONFIG_SIGNATURES.get(sig)
    # Use compare_digest to avoid timing attacks
    return hmac.compare_digest(expected or "", filename)

def handle_config_file(filename: str, sig: str) -> Optional[Dict]:
    """
    Read a configuration file after authenticating its signature.

    Parameters
    ----------
    filename : str
        Name of the configuration file to read.
    sig : str
        Cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid;
        otherwise, ``None``.
    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # 1. Verify that the signature is trusted for this file
    if not _signature_matches(sig, filename):
        # Signature does not match the expected value for this file
        return None

    # 2. Ensure the file exists and is readable
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' is missing.")

    try:
        with open(filename, "r", encoding="utf-8") as fp:
            # 3. Parse the file contents (JSON assumed)
            config_data = json.load(fp)

        # 4. Basic sanity check: configuration must be a dict
        if not isinstance(config_data, dict):
            return None

        return config_data

    except (OSError, json.JSONDecodeError) as exc:
        # Propagate file I/O errors; malformed JSON returns None
        if isinstance(exc, OSError):
            raise IOError(f"Error reading configuration file '{filename}': {exc}") from exc
        return None