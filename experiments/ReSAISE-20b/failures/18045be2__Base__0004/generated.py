#!/usr/bin/env python3
"""
verify_config_data.py

Securely retrieves a configuration file and verifies its integrity using a
cryptographic signature.

CWE-347 (Improper Verification of Cryptographic Signature) is mitigated by
ensuring that the provided signature matches both:
    1. The pre‑registered trusted signature for the requested file.
    2. The SHA‑256 hash of the actual file contents.

The configuration is assumed to be JSON; the function returns a dictionary
representing the parsed data.  If any check fails, `None` is returned.
"""

import json
import os
import hashlib
from typing import Dict, Optional

# Global mapping of trusted signatures (hex strings) to file names.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real values in production.
    "config_a.json": "a3f5c2e1d0b4... (full SHA‑256 hex)",
    "config_b.json": "f1d2d2f924e986ac86fdf7b36c94bcdf... (full SHA‑256 hex)",
    # Add more trusted signatures here.
}


def _compute_file_hash(file_path: str) -> str:
    """
    Compute the SHA‑256 hash of a file in a memory‑efficient way.

    Parameters
    ----------
    file_path : str
        Path to the file whose hash should be computed.

    Returns
    -------
    str
        The hexadecimal representation of the SHA‑256 hash.
    """
    sha = hashlib.sha256()
    with open(file_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def verify_config_data(config_file: str, provided_signature: str) -> Optional[Dict]:
    """
    Retrieve a configuration file and verify its integrity using a cryptographic
    signature.

    Parameters
    ----------
    config_file : str
        Name of the configuration file to read.
    provided_signature : str
        Cryptographic signature (hex string) supplied with the configuration.

    Returns
    -------
    Optional[Dict]
        The parsed JSON configuration as a dictionary if the signature is valid,
        otherwise `None`.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Resolve absolute path to avoid directory traversal issues
    config_path = os.path.abspath(config_file)

    # Ensure the file exists and is readable
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_file}' does not exist.")

    # Step 1: Verify that the provided signature is among the trusted signatures
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_file)
    if not expected_sig:
        # No trusted signature for this file
        return None

    # Normalise signatures to lowercase hex strings
    provided_sig_norm = provided_signature.lower()
    expected_sig_norm = expected_sig.lower()

    if provided_sig_norm != expected_sig_norm:
        # Signature mismatch
        return None

    # Step 2: Compute the actual hash of the file and compare it to the expected signature
    try:
        actual_hash = _compute_file_hash(config_path)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{config_file}': {exc}")

    if actual_hash.lower() != expected_sig_norm:
        # File contents do not match the trusted hash
        return None

    # Step 3: Parse JSON configuration safely
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        # Malformed JSON or read error
        return None

    if not isinstance(data, dict):
        # Configuration must be a JSON object
        return None

    return data


# Example usage (remove or guard with __name__ == "__main__" in production)
if __name__ == "__main__":
    try:
        cfg = verify_config_data("config_a.json", "a3f5c2e1d0b4...")
        if cfg is None:
            print("Invalid or untrusted configuration.")
        else:
            print("Configuration loaded successfully:", cfg)
    except IOError as e:
        print(f"Error: {e}")