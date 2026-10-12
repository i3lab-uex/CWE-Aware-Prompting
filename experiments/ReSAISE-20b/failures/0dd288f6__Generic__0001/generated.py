import hashlib
import json
from pathlib import Path

# Global dictionary mapping configuration file names to their expected SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example:
    # "app_config.json": "a3b1c5d2e6f7...",
}

def _compute_file_hash(path: Path) -> str:
    """
    Compute the SHA‑256 hash of a file and return it as a hex string.
    """
    sha = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def apply_config_data(configuration_name: str, config_signature: str):
    """
    Load a configuration file after validating its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        Name of the configuration file to load (e.g., 'app_config.json').
    config_signature : str
        The expected cryptographic signature (hex string) of the file.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found.
    """
    config_path = Path(configuration_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Compute the actual hash of the file
    actual_hash = _compute_file_hash(config_path)

    # Verify against the trusted signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)

    if not expected_signature:
        # No trusted signature known – treat as invalid
        return None

    if actual_hash.lower() != expected_signature.lower():
        # Signature mismatch – reject the configuration
        return None

    # At this point, the signature is valid; load and return the config
    with config_path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If JSON is malformed, treat as invalid
            return None