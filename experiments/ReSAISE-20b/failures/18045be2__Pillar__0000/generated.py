import json
from pathlib import Path
import hmac

# Global mapping of trusted signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – in real use these would be actual secure signatures.
    "config_a.json": "a1b2c3d4e5f6g7h8i9j0",
    "config_b.json": "1234567890abcdef1234",
}

def verify_config_data(config_file: str, provided_signature: str):
    """
    Retrieve a configuration file and verify that the supplied signature is
    trusted for this file.

    Parameters
    ----------
    config_file : str
        Name of the configuration file to load.
    provided_signature : str
        Cryptographic signature supplied alongside the configuration.

    Returns
    -------
    dict or None
        The parsed configuration data if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Resolve path and ensure the file exists
    config_path = Path(config_file)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_file}' not found")

    # Load the configuration content
    try:
        with config_path.open("r", encoding="utf-8") as f:
            content = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to read configuration file '{config_file}': {exc}") from exc

    # Retrieve the trusted signature for this configuration file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_file)

    # If no trusted signature is defined, reject the configuration
    if expected_signature is None:
        return None

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(provided_signature, expected_signature):
        return None

    # All checks passed – return the configuration data
    return content