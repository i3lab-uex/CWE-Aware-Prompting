import hashlib
import json
from pathlib import Path

# Example trusted signatures (filename -> SHA-256 hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "3f5c6d1e8a9b2c4f7e0d1a3b5c6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e",
    # add more entries as needed
}


def apply_config_data(configuration_name: str, config_signature: str) -> dict | None:
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The filename of the configuration file to load.
    config_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is verified, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve the file path relative to this script's directory
    config_path = Path(__file__).parent / configuration_name

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    try:
        with config_path.open("rb") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{configuration_name}': {exc}") from exc

    # Compute SHA-256 hash of the file content
    sha256 = hashlib.sha256()
    sha256.update(content)
    computed_hash = sha256.hexdigest()

    # Verify the provided signature against the trusted value
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_signature is None:
        # No trusted signature available; treat as invalid
        return None

    if not hashlib.compare_digest(computed_hash, expected_signature):
        # Signature mismatch
        return None

    # Verify that the provided config_signature matches the computed one
    if not hashlib.compare_digest(computed_hash, config_signature):
        # Provided signature does not match file content
        return None

    # Parse JSON safely; if parsing fails, treat as invalid
    try:
        config_data = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    # Ensure the result is a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data