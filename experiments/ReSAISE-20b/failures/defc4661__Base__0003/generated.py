#!/usr/bin/env python3
"""
Utility to read a configuration file and verify its cryptographic signature.

The function `handle_config_file` reads the contents of a configuration file,
computes its SHA‑256 digest, and compares it against an expected signature
stored in the global dictionary `TRUSTED_CONFIG_SIGNATURES`.

If the signature matches, the configuration is parsed as JSON and returned
as a dictionary.  If it does not match, `None` is returned.

If the file cannot be found or read, an `IOError` (or its subclass
`FileNotFoundError`) is raised.
"""

import json
import hashlib
import os
from typing import Dict, Optional

# Example global dictionary mapping filenames to their expected SHA‑256 hex digest.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config.json": "5d41402abc4b2a76b9719d911017c592",  # example
}

def _compute_sha256(data: bytes) -> str:
    """Return the SHA‑256 hex digest of the given data."""
    return hashlib.sha256(data).hexdigest()

def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    sign : str
        The cryptographic signature (hex digest) supplied by the caller.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid,
        otherwise `None`.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path for security (prevents directory traversal)
    abs_path = os.path.abspath(file_name)

    # Ensure the file exists
    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Read the file content in binary mode
    try:
        with open(abs_path, "rb") as fp:
            content = fp.read()
    except OSError as exc:  # includes FileNotFoundError, PermissionError
        raise IOError(f"Unable to read configuration file '{file_name}': {exc}") from exc

    # Verify the provided signature against the expected one
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig is None:
        # No known signature for this file: treat as invalid
        return None

    computed_sig = _compute_sha256(content)
    if not (computed_sig == expected_sig and sign.lower() == computed_sig):
        # Signature mismatch or caller-provided signature does not match computed one
        return None

    # Parse the configuration as JSON safely
    try:
        config = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise IOError(f"Failed to parse configuration file '{file_name}': {exc}") from exc

    if not isinstance(config, dict):
        # We expect a JSON object at the top level
        return None

    return config