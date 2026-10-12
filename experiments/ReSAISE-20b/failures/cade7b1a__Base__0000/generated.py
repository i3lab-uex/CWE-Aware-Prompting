import json
import hashlib
from pathlib import Path
from typing import Dict, Optional

# Global trusted signatures: mapping from config file name to its SHA-256 hex digest
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries (these should be replaced with real values)
    "app_settings.json": "d2c3f6b5e9a7f4c8d1b0e3a2f9c6d5b4a7e8f9c1d2b3a4e5f6g7h8i9j0k1l2m3",
    "db_config.json":   "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
    # Add more trusted signatures here
}


def _compute_sha256(file_path: Path) -> str:
    """Compute the SHA-256 hex digest of a file."""
    sha = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def process_config_data(config_name: str, signature: str) -> Optional[Dict]:
    """
    Load a JSON configuration file and verify its SHA-256 signature.

    Parameters
    ----------
    config_name : str
        The filename of the configuration to load.
    signature : str
        The cryptographic signature (hex digest) that accompanies the file.

    Returns
    -------
    dict | None
        The parsed JSON configuration if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    config_path = Path(config_name)

    # Ensure the file exists and is readable
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Compute the actual signature of the file
    try:
        computed_sig = _compute_sha256(config_path)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to compute signature for '{config_name}': {exc}")

    # Verify that the provided signature matches both the computed one
    # and the trusted signature stored in the global dictionary.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not expected_sig:
        # No trusted signature known for this config
        return None

    # Use constant-time comparison to avoid timing attacks
    if not hashlib.compare_digest(computed_sig, signature):
        return None

    if not hashlib.compare_digest(computed_sig, expected_sig):
        return None

    # Load and return the configuration data
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # pragma: no cover
        raise IOError(f"Failed to parse JSON in '{config_name}'.")