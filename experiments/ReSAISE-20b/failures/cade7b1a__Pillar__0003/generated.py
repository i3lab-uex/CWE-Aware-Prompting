import json
import hashlib
import hmac
from pathlib import Path
from typing import Dict, Optional

# Global dictionary mapping configuration file names to trusted SHA‑256 signatures
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with actual trusted signatures
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "db_config.json":  "5d41402abc4b2a76b9719d911017c592",
}


def _compute_sha256(file_path: Path) -> str:
    """Return the SHA‑256 hex digest of the file's contents."""
    hasher = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def process_config_data(config_name: str, signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load (relative to the current working directory).
    signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    config_path = Path(config_name)

    # Ensure the file exists and is readable
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Compute the actual SHA‑256 signature of the file
    try:
        actual_signature = _compute_sha256(config_path)
    except Exception as exc:
        raise IOError(f"Failed to read configuration file '{config_name}': {exc}") from exc

    # Verify the provided signature against the trusted value
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not trusted_sig:
        # No trusted signature registered for this file – reject
        return None

    if not hmac.compare_digest(actual_signature, trusted_sig):
        # Signature mismatch – reject
        return None

    # Signature is valid – load and return the configuration as a dictionary
    try:
        with config_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        # Malformed JSON – treat as failure
        return None
    except Exception as exc:
        raise IOError(f"Error loading configuration file '{config_name}': {exc}") from exc