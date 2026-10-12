#!/usr/bin/env python3
"""
Utility to load configuration files with cryptographic signature verification.

The module defines a single public function:
    handle_config_data(file_name: str, file_signature: str) -> Optional[dict]

The function reads the JSON configuration from *file_name*, verifies that
the SHA‑256 hash of its contents matches *file_signature* (using a constant‑time
comparison), and returns the parsed configuration dictionary.
If the file does not exist an IOError is raised.  If the signature does not
match, None is returned.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Global dictionary containing the trusted signatures for known configuration
# files.  In a real system this would be populated from a secure source or
# environment variable.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entry:
    # "app_config.json": "<sha256-hash-of-file>",
}

# --------------------------------------------------------------------------- #
def _compute_sha256(data: bytes) -> str:
    """Return the hexadecimal SHA‑256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def handle_config_data(file_name: str, file_signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Path to the JSON configuration file.
    file_signature : str
        Expected SHA‑256 hash of the file contents (hex string).

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If *file_name* does not exist or cannot be read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    try:
        with open(file_name, "rb") as f:
            raw_data = f.read()
    except OSError as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc

    # Compute the hash of the raw data
    computed_hash = _compute_sha256(raw_data)

    # Constant‑time comparison to mitigate timing attacks (CWE-345)
    if not hmac.compare_digest(computed_hash, file_signature):
        return None

    # Parse JSON safely; any parsing error results in a None return
    try:
        config = json.loads(raw_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    if not isinstance(config, dict):  # pragma: no cover
        return None

    return config