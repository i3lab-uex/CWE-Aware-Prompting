import json
import hmac
from typing import Dict, Optional

# Global dictionary mapping known good signatures to filenames.
# In practice these would be derived from a secure signing process
# (e.g., HMAC or asymmetric signatures). Here we assume they are raw hex strings.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # signature : filename
    "a1b2c3d4e5f6g7h8i9j0": "config.yaml",
    # Add more trusted signatures here...
}

def handle_config_file(filename: str, sig: str) -> Optional[Dict]:
    """
    Read a configuration file and return its contents as a dictionary
    only if the provided signature matches a trusted entry.

    Args:
        filename: Name of the configuration file to read.
        sig: Cryptographic signature supplied with the configuration.

    Returns:
        The parsed configuration as a dictionary if the signature is valid,
        otherwise None.

    Raises:
        IOError: If the requested configuration file cannot be read.
    """
    # 1. Verify that the supplied signature is known and matches this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if not expected_sig:
        # No trusted signature for this file
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑347)
    if not hmac.compare_digest(expected_sig, sig):
        return None

    # 2. Read the configuration file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError as e:
        raise IOError(f"Configuration file '{filename}' not found") from e

    # 3. Parse the configuration data
    # Assume JSON format; adapt as needed for other formats (YAML, INI, etc.)
    try:
        config = json.loads(data)
    except json.JSONDecodeError as e:
        # Invalid format – treat as authentication failure
        return None

    return config