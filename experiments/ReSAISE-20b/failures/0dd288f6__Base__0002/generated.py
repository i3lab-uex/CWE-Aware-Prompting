import json
import hashlib
import hmac
from pathlib import Path

# Global mapping of configuration filenames to their expected signatures (hex digests)
TRUSTED_CONFIG_SIGNATURES = {
    # Example: "app_config.json": "a1b2c3d4e5f6...",
}

def _compute_file_signature(file_path: Path) -> str:
    """
    Compute the SHA-256 digest of a file's contents and return it as a hex string.
    """
    sha256 = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def apply_config_data(configuration_name: str, config_signature: str):
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The name of the configuration file (relative to the current working directory).
    config_signature : str
        The cryptographic signature provided for the configuration file.

    Returns
    -------
    dict | None
        The parsed JSON configuration if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or accessed.
    """
    config_path = Path(configuration_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found")

    # Compute the actual signature of the file
    actual_signature = _compute_file_signature(config_path)

    # Use a timing‑attack resistant comparison
    if not hmac.compare_digest(actual_signature, config_signature):
        return None

    # If the signature matches, parse and return the JSON content
    try:
        with config_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}") from exc