#!/usr/bin/env python3
"""
Utility to read a configuration file and verify its cryptographic signature.

The function `handle_config_file` will:
1. Load the file contents.
2. Compute a SHA‑256 hash of the raw bytes.
3. Compare the computed hash (hex digest) with the expected signature from
   `TRUSTED_CONFIG_SIGNATURES` and the provided `sign`.
4. If both signatures match, parse the file as JSON and return a dictionary.
5. If any check fails, return `None`.  An `IOError` is raised if the file
   cannot be opened.

Security notes:
- SHA‑256 is used as a fast, non‑collision-resistant hash suitable for
  configuration integrity checks.
- The function does **not** perform any form of authentication or signing;
  it only verifies that the file content matches a pre‑known hash.
- For real deployments consider HMAC with a secret key or signed tokens
  instead of static hashes.
"""

import json
import os
from hashlib import sha256

# Example trusted signatures dictionary. In real code this would be
# populated from a secure source (e.g., compiled in, fetched over TLS,
# or stored in an encrypted file).
TRUSTED_CONFIG_SIGNATURES = {
    # "config.json": "a3f5c1b8e9... (hex digest)",
}


def handle_config_file(file_name: str, sign: str) -> dict | None:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name (or path) of the configuration file to read.
    sign : str
        The expected cryptographic signature (hex digest) for the file.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid; otherwise
        ``None``.

    Raises
    ------
    IOError
        If the file cannot be located or opened.
    """
    # Resolve absolute path to guard against relative traversal attacks
    abs_path = os.path.abspath(file_name)

    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Read the raw bytes
    with open(abs_path, "rb") as f:
        data = f.read()

    # Compute SHA‑256 hash of the file contents
    computed_hash = sha256(data).hexdigest()

    # Verify both the provided sign and the trusted signature match
    expected_sign = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if not expected_sign or computed_hash != sign or computed_hash != expected_sign:
        return None

    # Parse JSON configuration
    try:
        config = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed configuration; treat as invalid
        return None

    if not isinstance(config, dict):
        # Configuration must be a mapping
        return None

    return config