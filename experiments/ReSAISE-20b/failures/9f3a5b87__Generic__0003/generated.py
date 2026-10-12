import json
import hashlib
from pathlib import Path
from typing import Dict, Optional

# Example trusted signatures dictionary.  In a real system this would be
# populated from a secure source.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # SHA-256
    "db_config.json":   "5d41402abc4b2a76b9719d911017c592",
    # add more filenames and their expected SHA‑256 hex digests here
}


def _compute_file_hash(file_path: Path) -> str:
    """Return the SHA‑256 hex digest of *file_path*."""
    sha = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def handle_config_data(file_name: str, file_signature: str) -> Optional[Dict]:
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    file_signature : str
        Cryptographic signature (hex digest) supplied alongside the data.

    Returns
    -------
    dict | None
        The parsed configuration as a dictionary if the signature matches.
        `None` is returned if the signature does not match or parsing fails.

    Raises
    ------
    IOError
        If *file_name* does not exist.
    """
    file_path = Path(file_name)

    if not file_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Compute the actual hash of the file.
    real_hash = _compute_file_hash(file_path)

    # Retrieve the expected hash from the trusted list.
    expected_hash = TRUSTED_CONFIG_SIGNATURES.get(file_name)

    # If there is no entry for this file, we cannot trust it.
    if expected_hash is None:
        return None

    # Verify that the supplied signature matches both the trusted value
    # and the actual hash of the file.
    if (file_signature.lower() != expected_hash.lower()) or (real_hash.lower() != expected_hash.lower()):
        return None

    # Try to parse the file as JSON.
    try:
        with file_path.open("rt", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        # If parsing fails we consider the data invalid.
        return None