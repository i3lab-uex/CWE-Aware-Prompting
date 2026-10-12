import os
import json
import hashlib
from typing import Dict, Optional

# Example trusted signatures dictionary. In a real system this would be
# populated from a secure source.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config.json": "a3b1c2d4e5f6..." (hex digest)
}

def _compute_file_hash(path: str) -> str:
    """
    Compute the SHA‑256 hash of a file in a memory‑efficient way.
    Returns the hexadecimal digest string.
    """
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def _constant_time_compare(a: str, b: str) -> bool:
    """
    Perform a constant‑time comparison of two strings to mitigate timing attacks.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> Optional[Dict]:
    """
    Verify the cryptographic signature of a configuration file before loading it.

    Parameters
    ----------
    cfg_name : str
        The name of the configuration file (relative to the current working directory).
    cfg_signature : str
        The expected cryptographic signature (hex digest) of the configuration file.

    Returns
    -------
    dict | None
        The parsed JSON configuration if the signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path for security
    cfg_path = os.path.abspath(cfg_name)

    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_name}' does not exist.")

    # Compute the actual hash of the file
    try:
        actual_hash = _compute_file_hash(cfg_path)
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{cfg_name}': {exc}") from exc

    # Retrieve the trusted hash for this configuration
    trusted_hash = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if trusted_hash is None:
        raise ValueError(f"No trusted signature available for '{cfg_name}'.")

    # Compare hashes in constant time
    if not _constant_time_compare(actual_hash, trusted_hash):
        # Signature mismatch: do not load the configuration
        return None

    # Verify that the provided cfg_signature matches the trusted hash as well
    if not _constant_time_compare(cfg_signature.lower(), trusted_hash.lower()):
        # The caller supplied an incorrect signature
        return None

    # Load and return the configuration (assumed to be JSON)
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to parse configuration file '{cfg_name}': {exc}") from exc

    return config