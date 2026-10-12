import json
import os
from typing import Dict, Optional

# Example trusted signatures dictionary.
# In a real application this would be securely populated from
# a signed source or environment variable.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "app_config.json": "d41d8cd98f00b204e9800998ecf8427e",
    # Add more trusted filenames and their signatures here.
}


def validate_config_file(
    filename: str, cryptographic_signature: str
) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    filename : str
        Name of the configuration file to load.
    cryptographic_signature : str
        Signature that was sent with the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature matches
        a trusted value; otherwise, ``None``.
    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Verify the signature against the trusted list
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if not expected_signature or cryptographic_signature != expected_signature:
        # Signature mismatch – do not expose configuration
        return None

    # Load the configuration data (JSON format assumed)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(
            f"Failed to read configuration file '{filename}': {exc}"
        ) from exc

    if not isinstance(config, dict):
        # Configuration must be a dictionary
        return None

    return config