import json
import hashlib
from pathlib import Path

# Global dictionary mapping configuration file names to their trusted SHA‑256 signatures (hex)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "d2c1f6a3b9e5... (example)",
    # Add more entries as needed
}

def apply_config_data(configuration_name: str, config_signature: str) -> dict | None:
    """
    Load a configuration file and verify its authenticity.

    Parameters
    ----------
    configuration_name : str
        The name of the configuration file (relative to current working directory).
    config_signature : str
        The SHA‑256 signature supplied by the caller.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches; otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    config_path = Path(configuration_name)

    # Ensure the file exists and is readable
    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Compute the SHA‑256 hash of the file contents
    try:
        with config_path.open("rb") as f:
            data = f.read()
            computed_hash = hashlib.sha256(data).hexdigest()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}") from exc

    # Verify the supplied signature matches the computed hash
    if config_signature.lower() != computed_hash:
        # Signature mismatch – do not load the configuration
        return None

    # Verify the signature against the trusted list (optional double‑check)
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_signature and config_signature.lower() != expected_signature.lower():
        # The supplied signature does not match the trusted one
        return None

    # Parse JSON safely
    try:
        config = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise IOError(f"Configuration file '{configuration_name}' is not valid JSON: {exc}") from exc

    return config