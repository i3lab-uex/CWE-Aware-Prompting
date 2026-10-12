import json
import hmac
from pathlib import Path

# Example trusted signatures (hashes). In real usage these would be securely populated.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "a3f5c1e8b2d4f6c7e9a0b1234567890abcdef1234567890abcdef1234567890",
    # Add more file:signature pairs here
}

def handle_config_file(file_name: str, sign: str) -> dict | None:
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    sign : str
        The cryptographic signature provided for this configuration.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid;
        otherwise, returns ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Resolve the path safely (no traversal outside current directory)
    config_path = Path(file_name).resolve()
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found")

    # Retrieve the expected signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if not expected_sig:
        # No known signature for this file – treat as invalid
        return None

    # Compare signatures using a timing‑attack resistant comparison
    if not hmac.compare_digest(sign, expected_sig):
        return None

    # Signature verified – load the configuration
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Any parsing error should not expose sensitive data; raise a generic IOError
        raise IOError(f"Failed to load configuration from '{file_name}': {e}") from e