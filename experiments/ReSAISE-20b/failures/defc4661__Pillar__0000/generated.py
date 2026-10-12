#!/usr/bin/env python3
"""
Utility to securely load a configuration file and verify its cryptographic signature.
"""

import json
import hashlib
import hmac
from pathlib import Path
from typing import Dict, Optional

# Example trusted signatures mapping (filename -> hex‑encoded SHA‑256)
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config.json": "a3f5c6e2b1d4... (full 64‑char hex string)"
}

def _compute_file_hash(file_path: Path) -> str:
    """
    Compute the SHA‑256 hash of a file in a memory‑efficient way.
    Returns the hexadecimal digest string.
    """
    sha256 = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Load a JSON configuration file and verify its signature.

    Args:
        file_name: Name of the configuration file (relative to current working directory).
        sign: Hex‑encoded SHA‑256 signature that should match the file contents.

    Returns:
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises:
        IOError: If the file cannot be read or does not exist.
    """
    # Resolve the path and ensure it exists
    config_path = Path(file_name).expanduser().resolve()
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found")

    # Compute the hash of the file contents
    computed_hash = _compute_file_hash(config_path)

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_hash, sign.lower()):
        # Signature mismatch – do NOT load the configuration
        return None

    # If the signature is trusted, parse and return the JSON content
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        # Corrupted JSON – treat it as an invalid configuration
        raise IOError(f"Failed to parse JSON in '{file_name}': {exc}") from exc


# Example usage (commented out – remove when integrating)
# if __name__ == "__main__":
#     try:
#         cfg = handle_config_file("config.json", TRUSTED_CONFIG_SIGNATURES["config.json"])
#         if cfg is None:
#             print("Signature verification failed.")
#         else:
#             print("Configuration loaded:", cfg)
#     except IOError as e:
#         print(e)