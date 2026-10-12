#!/usr/bin/env python3
"""
verify_config_data – Load and verify a configuration file using its cryptographic signature.

The function ensures that the requested configuration file exists in a known directory,
that the supplied signature matches the trusted one, and that the content is parsed
as JSON before being returned.  It uses constant‑time comparison to mitigate timing attacks
(CWE‑693).
"""

import json
import os
from pathlib import Path
import hmac

# Global mapping of configuration file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "a1b2c3d4e5f678901234567890abcdef12345678",
    "db_config.json":  "b2c3d4e5f678901234567890abcdef12345678a1",
    # Add more trusted signatures here
}

# Base directory where configuration files are stored.
CONFIG_DIR = Path("/etc/myapp/config").resolve()


def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Load and verify a configuration file.

    Parameters
    ----------
    config_file : str
        Name of the configuration file to retrieve (relative path only).
    provided_signature : str
        Cryptographic signature supplied alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed JSON configuration if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be accessed.
    """

    # 1. Ensure that the filename contains no path traversal components.
    if os.path.isabs(config_file) or ".." in Path(config_file).parts:
        raise ValueError("Invalid configuration file name")

    # 2. Resolve the absolute path and ensure it is inside CONFIG_DIR.
    config_path = (CONFIG_DIR / config_file).resolve()
    if not str(config_path).startswith(str(CONFIG_DIR)):
        raise ValueError("Configuration file is outside the allowed directory")

    # 3. Check that the file exists and can be read.
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_file}' is missing")

    # 4. Verify the signature against the trusted mapping.
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_file)
    if expected_signature is None:
        # Unknown configuration file – treat as untrusted.
        return None

    if not hmac.compare_digest(provided_signature, expected_signature):
        # Signature does not match – do not load the configuration.
        return None

    # 5. Read and parse the JSON content safely.
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # Treat any read/parse error as a failure to load configuration.
        raise IOError(f"Failed to load configuration '{config_file}': {exc}") from exc

    # 6. Return the parsed configuration dictionary.
    return data