#!/usr/bin/env python3
"""
Utility for securely loading and validating configuration files.
"""

import json
import hashlib
import hmac
from pathlib import Path

# Global mapping of configuration file names to their expected SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (replace with real values)
    "app_config.json": "d2c7e3b8a1f4e5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8g9h0",
    "db_config.json":  "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8g9h0d2c7e3b8a1f4e5b6c7d8e9",
}

def _compute_sha256(file_path: Path) -> str:
    """
    Compute the SHA‑256 hex digest of a file in a memory‑efficient manner.
    """
    sha = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Load a configuration file after verifying its SHA‑256 signature.

    Parameters
    ----------
    cfg_name : str
        Name of the configuration file (e.g., "app_config.json").
    cfg_signature : str
        The signature that should match the file's SHA‑256 digest.

    Returns
    -------
    dict | None
        Parsed JSON configuration if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be opened.
    """
    # Ensure that the supplied name is trusted
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if expected_sig is None:
        raise ValueError(f"Configuration file '{cfg_name}' is not in the trusted list.")

    # Resolve path relative to the current working directory
    config_path = Path(cfg_name)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{cfg_name}' cannot be located.")

    # Compute the actual signature
    actual_sig = _compute_sha256(config_path)

    # Securely compare signatures to avoid timing attacks
    if not hmac.compare_digest(actual_sig, expected_sig):
        # Signature mismatch; do not load the file
        return None

    # Load and parse JSON configuration
    try:
        with config_path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        # Corrupt or invalid JSON – treat as an untrusted configuration
        raise ValueError(f"Invalid JSON in '{cfg_name}': {exc}") from exc

# Example usage (commented out to avoid side effects during import)
# if __name__ == "__main__":
#     cfg = verify_configuration_file("app_config.json", TRUSTED_CONFIG_SIGNATURES["app_config.json"])
#     if cfg is not None:
#         print("Configuration loaded:", cfg)