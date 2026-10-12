import json
import hashlib
import hmac
from pathlib import Path

# Example trusted signatures dictionary (filename -> hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd5c1a2e7f9b8c1e9ed",
    # add more entries as needed
}


def apply_config_data(configuration_name: str, config_signature: str):
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        Name of the configuration file to load.
    config_signature : str
        Expected cryptographic signature (hex string) for the file.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature matches;
        otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve path relative to current working directory
    config_path = Path(configuration_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found")

    try:
        # Read the raw bytes of the configuration file
        with config_path.open("rb") as f:
            data = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{configuration_name}': {exc}") from exc

    # Compute SHA-256 digest of the file contents
    computed_digest = hashlib.sha256(data).hexdigest()

    # Compare using constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_digest, config_signature):
        # Signature mismatch – do not expose details to the caller
        return None

    # Parse JSON configuration into a dictionary
    try:
        config_dict = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # If parsing fails, treat it as an invalid configuration
        return None

    return config_dict