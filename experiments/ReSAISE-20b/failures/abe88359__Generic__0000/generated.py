import os
import json
import hashlib
import hmac

# Global mapping of filenames to their trusted SHA‑256 signatures
TRUSTED_CONFIG_SIGNATURES = {
    # example entries
    "app_config.json": "3f5c1e2b9d4a... (full hex signature)",
    # add more entries as needed
}

def _compute_sha256(data: bytes) -> str:
    """Return the hex digest of SHA‑256 for the given data."""
    return hashlib.sha256(data).hexdigest()

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        Name (or relative path) of the configuration file.
    cfg_signature : str
        The signature provided by the caller (hex string).

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature matches, otherwise `None`.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path for safety
    cfg_path = os.path.abspath(cfg_name)

    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_name}' not found.")

    try:
        with open(cfg_path, "rb") as fp:
            data = fp.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    # Compute the signature of the file content
    computed_sig = _compute_sha256(data)

    # Securely compare signatures to avoid timing attacks
    if not hmac.compare_digest(computed_sig, cfg_signature):
        return None

    # Optionally cross‑check against the trusted list
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(os.path.basename(cfg_name))
    if expected_sig and not hmac.compare_digest(computed_sig, expected_sig):
        return None

    # Parse JSON content; raise ValueError if invalid
    try:
        config = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Invalid configuration format in '{cfg_name}': {exc}") from exc

    return config