import os
import json
import hashlib
import hmac

# Example trusted signatures dictionary. In real use this would be securely populated.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "3f2e8c1d9a4b6f7e0d1c2b3a4e5f6a7b8c9d0e1f2a3b4c5d6e7f8g9h0i1j2k3l",
    # Add more entries as needed
}


def _compute_signature(file_path: str) -> str:
    """
    Compute a SHA-256 hex digest of the file contents.
    """
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name of the configuration file to read.
    cfg_signature : str
        The expected cryptographic signature (hex digest) of the file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path relative to current working directory
    cfg_path = os.path.abspath(cfg_name)

    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_name}' not found.")

    # Compute the actual signature
    try:
        actual_sig = _compute_signature(cfg_path)
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{cfg_name}': {exc}") from exc

    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(actual_sig, cfg_signature):
        return None

    # Parse the JSON configuration
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to parse configuration file '{cfg_name}': {exc}") from exc

    return config