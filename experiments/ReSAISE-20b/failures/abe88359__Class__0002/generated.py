import json
import hashlib
import hmac
from pathlib import Path
from typing import Dict, Optional

# Global dictionary mapping configuration filenames to their expected SHA‑256 signatures
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values)
    "app_config.json": "d2c7e1b4f5a9c3b8e6f9d2e4a1c0b7e5d3f2a1b4c6d8e9f0a1b2c3d4e5f67890",
    # Add more entries as needed
}

def _compute_file_hash(file_path: Path) -> str:
    """Compute the SHA‑256 hash of a file in a memory‑efficient manner."""
    sha = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> Optional[Dict]:
    """
    Verify the integrity and authenticity of a configuration file.

    Parameters
    ----------
    cfg_name : str
        The filename (relative to the configuration directory) of the config file.
    cfg_signature : str
        The expected cryptographic signature (hex string) of the config file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve the path safely relative to a known configuration directory
    config_dir = Path(__file__).parent / "config"
    cfg_path = (config_dir / cfg_name).resolve()

    # Prevent path traversal: ensure the resolved path is still inside config_dir
    if not cfg_path.is_file() or cfg_path.parent != config_dir:
        raise IOError(f"Configuration file '{cfg_name}' not found or is outside the allowed directory.")

    # Compute the hash of the file
    try:
        actual_hash = _compute_file_hash(cfg_path)
    except Exception as exc:
        raise IOError(f"Failed to read configuration file '{cfg_name}': {exc}") from exc

    # Compare the computed hash with the supplied signature using constant‑time comparison
    if not hmac.compare_digest(actual_hash.lower(), cfg_signature.lower()):
        # Signature mismatch – treat as invalid configuration
        return None

    # Optionally, verify that the signature matches the trusted list for this file
    expected_trusted = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if expected_trusted and not hmac.compare_digest(actual_hash.lower(), expected_trusted.lower()):
        # The file matches the supplied signature but not the trusted one – reject
        return None

    # Parse and return the configuration as a dictionary
    try:
        with cfg_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise IOError(f"Failed to parse configuration file '{cfg_name}': {exc}") from exc