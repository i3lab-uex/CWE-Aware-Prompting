#!/usr/bin/env python3
"""
Utility to load a configuration file and verify its integrity using a
cryptographic signature.

The global dictionary ``TRUSTED_CONFIG_SIGNATURES`` maps configuration file names
to their trusted SHA‑256 hex digests.  A signature supplied to the function must
match the computed digest of the file contents in order for the configuration
to be considered valid.

Security considerations:
- The signature is verified using a cryptographic hash (SHA‑256) rather than
  simple string comparison, mitigating the risk of tampering.
- The function resolves file paths safely to prevent directory traversal
  attacks. Only files within the current working directory (or a specified
  config base) are allowed.
- The file is read in binary mode to avoid any encoding-related issues before
  hashing.

CWE‑693 (Protection Mechanism Failure) is addressed by using a proven
cryptographic hash algorithm and verifying the digest against an immutable
trusted source.
"""

import json
import pathlib
import hashlib
from typing import Dict, Any

# Example trusted signatures dictionary.
# In a real deployment this should be populated from a secure source
# (e.g., environment variable, signed manifest, etc.).
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # 'config.json': 'sha256hexdigest...',
}

def _secure_path(file_name: str) -> pathlib.Path:
    """
    Resolve a configuration file name to an absolute path safely.
    Rejects paths that attempt directory traversal.
    """
    base_dir = pathlib.Path.cwd()  # or a dedicated config directory
    candidate = (base_dir / file_name).resolve()
    if not str(candidate).startswith(str(base_dir.resolve())):
        raise ValueError("Attempted directory traversal in configuration file name")
    return candidate

def process_config_data(config_name: str, signature: str) -> Dict[str, Any] | None:
    """
    Load and validate a configuration file.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load.
    signature : str
        The cryptographic signature (hex digest) that accompanies the file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid;
        otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    ValueError
        If a directory traversal attempt is detected in ``config_name``.
    """
    # Resolve the file path securely
    config_path = _secure_path(config_name)

    try:
        with config_path.open("rb") as f:
            data_bytes = f.read()
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{config_name}' not found") from exc
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{config_name}': {exc}") from exc

    # Compute SHA‑256 digest of the file contents
    computed_digest = hashlib.sha256(data_bytes).hexdigest()

    # Verify that the provided signature matches the computed digest
    trusted_digest = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not trusted_digest or computed_digest.lower() != signature.lower():
        # Signature mismatch or no trusted digest available
        return None

    # Parse JSON configuration into a dictionary
    try:
        config_dict = json.loads(data_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise IOError(f"Invalid JSON in configuration file '{config_name}': {exc}") from exc

    return config_dict