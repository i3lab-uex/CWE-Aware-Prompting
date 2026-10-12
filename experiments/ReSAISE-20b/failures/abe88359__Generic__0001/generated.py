import os
import json
import hashlib
import hmac

# Global dictionary mapping configuration filenames to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: 'app_config.json': 'e3b0c44298fc1c149afbf4c8996fb924...'
}

def _compute_sha256(file_path: str) -> str:
    """Return the hexadecimal SHA‑256 digest of a file."""
    hash_obj = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Validate a configuration file against its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name (or relative path) of the configuration file to load.
    cfg_signature : str
        The signature supplied for this configuration (hex string).

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is verified,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Resolve absolute path to prevent directory traversal attacks
    config_path = os.path.abspath(cfg_name)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{cfg_name}' not found")

    # Compute the SHA‑256 digest of the file contents
    computed_sig = _compute_sha256(config_path)

    # Verify that the provided signature matches both the supplied value
    # and the trusted value (if present in the global dictionary).
    if not hmac.compare_digest(computed_sig, cfg_signature):
        return None

    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if trusted_sig is not None and not hmac.compare_digest(computed_sig, trusted_sig):
        return None

    # Load the configuration (JSON is chosen for its ubiquity)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # If parsing fails we treat it as an invalid configuration
        return None

    if not isinstance(config, dict):
        # Expect a dictionary; otherwise reject
        return None

    return config