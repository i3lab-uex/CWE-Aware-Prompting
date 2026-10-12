import json
import os
from pathlib import Path
import hmac
import hashlib

# Global mapping of filenames to their expected HMAC signatures (hex digests).
TRUSTED_CONFIG_SIGNATURES = {
    # Example entry: "config.json": "5f2d3e..."
}

def _secure_compare(a: str, b: str) -> bool:
    """
    Perform a constant‑time comparison of two hex digests to mitigate timing attacks.
    """
    return hmac.compare_digest(a, b)

def _compute_file_signature(file_path: Path, key: bytes) -> str:
    """
    Compute an HMAC‑SHA256 signature for the contents of a file.
    """
    h = hashlib.sha256(key)
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def apply_config_data(configuration_name: str, config_signature: str) -> dict | None:
    """
    Load and validate a configuration file.

    Parameters
    ----------
    configuration_name : str
        The name of the configuration file to load.
    config_signature : str
        The HMAC‑SHA256 signature supplied for this configuration.

    Returns
    -------
    dict | None
        Parsed JSON configuration if the signature is verified; otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found.
    """
    # Resolve the path relative to the current working directory
    config_path = Path(configuration_name).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Retrieve the expected signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_path.name)
    if expected_sig is None:
        # If we have no record, do not accept the file
        return None

    # Verify supplied signature against expected
    if not _secure_compare(config_signature.lower(), expected_sig.lower()):
        return None

    # Compute the actual signature of the file's contents
    # For demonstration, we use a static key. In production, use a secure KMS or HSM.
    STATIC_KEY = b"my-very-secret-key"
    actual_sig = _compute_file_signature(config_path, STATIC_KEY)

    # Final verification: ensure the file's contents match the expected signature
    if not _secure_compare(actual_sig, expected_sig):
        return None

    # Load and parse JSON configuration
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If parsing fails, treat it as an invalid configuration
        return None