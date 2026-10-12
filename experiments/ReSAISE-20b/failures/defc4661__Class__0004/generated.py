#!/usr/bin/env python3
"""
Utility for securely loading a configuration file with signature verification.
"""

import json
import os
from pathlib import Path
import hmac

# Global dictionary mapping file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: "app_config.json": "sha256:<hex_digest>"
}

def _compute_signature(file_path: Path) -> str:
    """
    Compute the SHA-256 digest of the file contents and return it in a
    standardized string format: "sha256:<hex_digest>".
    """
    import hashlib

    sha = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha.update(chunk)
    return f"sha256:{sha.hexdigest()}"


def handle_config_file(file_name: str, sign: str):
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name (or relative path) of the configuration file to load.
    sign : str
        The cryptographic signature provided for this configuration.

    Returns
    -------
    dict or None
        Parsed JSON configuration if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or accessed.
    """
    # Resolve absolute path and ensure it exists
    config_path = Path(file_name).expanduser().resolve()
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Verify the provided signature matches the trusted one
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_path.name)
    if not trusted_sig:
        # No signature known for this file; treat as untrusted
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sign, trusted_sig):
        return None

    # Optionally re‑compute the signature to double‑check (CWE-345 mitigation)
    computed_sig = _compute_signature(config_path)
    if not hmac.compare_digest(computed_sig, trusted_sig):
        return None

    # Load and parse the JSON configuration
    try:
        with config_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to read or parse configuration file: {exc}") from exc