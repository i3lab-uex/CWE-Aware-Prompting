import json
from pathlib import Path
import hashlib

# Global dictionary mapping configuration filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more filenames and their SHA‑256 signatures here
}

def _compute_signature(content: bytes) -> str:
    """Return the SHA‑256 hex digest of the given content."""
    return hashlib.sha256(content).hexdigest()

def apply_config_data(configuration_name: str, config_signature: str):
    """
    Load a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The name of the configuration file to load.
    config_signature : str
        The signature that should match the trusted value for this file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    config_path = Path(configuration_name)

    # Ensure the file exists and is readable
    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    try:
        content = config_path.read_bytes()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{configuration_name}': {exc}") from exc

    # Verify the provided signature against the trusted one
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_sig is None:
        # No trusted signature known for this file
        return None

    if config_signature.lower() != expected_sig.lower():
        # Signature mismatch – do not trust the content
        return None

    # Optionally, recompute signature to double‑check integrity
    computed_sig = _compute_signature(content)
    if config_signature.lower() != computed_sig.lower():
        # The content has changed since the signature was generated
        return None

    try:
        config_dict = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # Corrupted or non‑JSON configuration
        raise IOError(f"Invalid configuration format in '{configuration_name}': {exc}") from exc

    return config_dict