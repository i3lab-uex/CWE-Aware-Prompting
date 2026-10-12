import json
import hashlib
import hmac
from pathlib import Path

# Global dictionary mapping configuration filenames to their expected SHA‑256 signatures (hex)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more trusted config files and signatures here
}

def apply_config_data(configuration_name: str, config_signature: str):
    """
    Load a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The name of the configuration file to load.
    config_signature : str
        A cryptographic signature (hex string) provided by the caller.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if signature verification succeeds.
        Returns ``None`` if the provided signature does not match the trusted value.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve the path to the configuration file
    config_path = Path(configuration_name)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Read the raw bytes of the configuration
    try:
        raw_data = config_path.read_bytes()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}") from exc

    # Compute the SHA‑256 hash of the file contents
    actual_hash = hashlib.sha256(raw_data).hexdigest()

    # Retrieve the expected signature from the trusted list
    expected_hash = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)

    # If no entry exists in the trusted dictionary, treat it as untrusted
    if expected_hash is None:
        return None

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(actual_hash, expected_hash):
        # Signature does not match; do not return the configuration
        return None

    # The signature matches. Validate that the provided config_signature also matches.
    if not hmac.compare_digest(actual_hash, config_signature):
        # Caller provided an incorrect signature
        return None

    # Parse the configuration data as JSON. Raise a ValueError if parsing fails.
    try:
        config_dict = json.loads(raw_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Configuration file '{configuration_name}' contains invalid JSON: {exc}") from exc

    return config_dict