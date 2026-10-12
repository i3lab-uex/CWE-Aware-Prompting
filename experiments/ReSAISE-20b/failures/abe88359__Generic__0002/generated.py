#!/usr/bin/env python3
"""
Utility to read and verify configuration files against known cryptographic signatures.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional

# Example trusted signatures dictionary.
# In a real application this should be securely loaded from a protected source.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # 'config_name.json': 'sha256hexsignature...',
}

def _compute_sha256(file_path: Path) -> str:
    """Compute the SHA‑256 hash of a file's contents as a hex string."""
    sha = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def verify_configuration_file(cfg_name: str, cfg_signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name of the configuration file (including extension).
    cfg_signature : str
        The signature provided externally for verification.

    Returns
    -------
    dict or None
        Parsed configuration data if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    config_path = Path(cfg_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{cfg_name}' does not exist or is not a regular file.")

    # Compute the signature of the actual file contents.
    try:
        computed_sig = _compute_sha256(config_path)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to compute signature for '{cfg_name}': {exc}") from exc

    # Verify against the trusted signatures dictionary.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if expected_sig is None:
        # No trusted signature known for this file – treat as untrusted.
        return None

    if computed_sig != expected_sig or computed_sig != cfg_signature:
        # Signature mismatch – do not trust the configuration.
        return None

    # Load and parse the configuration (assumed to be JSON).
    try:
        with config_path.open("rt", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read or parse configuration '{cfg_name}': {exc}") from exc