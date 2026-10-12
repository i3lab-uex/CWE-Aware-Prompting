import json
import hmac
from pathlib import Path

# Example trusted signatures mapping (should be populated with real values)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "5e8c2a4f9d3b6a7c1d2e3f4g5h6i7j8k9l0m",
    # Add more filename:signature pairs here
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after validating its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Cryptographic signature provided for validation.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file does not exist.
    """
    # Resolve path and ensure file exists
    config_path = Path(config_filename)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Retrieve the expected signature for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # No known signature for this file – treat as invalid
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE-693)
    if not hmac.compare_digest(crypt_signature, expected_sig):
        return None

    # Load the configuration file (assumed to be JSON)
    try:
        with config_path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:  # pragma: no cover
        # If parsing fails, treat it as invalid config
        return None

    if not isinstance(data, dict):
        # Configuration must be a dictionary
        return None

    return data