import os
import json
import hashlib
import hmac

# Global dictionary mapping configuration file names to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more entries as needed
}


def _compute_sha256(data: bytes) -> str:
    """Compute the SHA‑256 hex digest of the given data."""
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()


def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Validate the authenticity of a configuration file.

    Parameters
    ----------
    cfg_name : str
        The name (or relative path) of the configuration file.
    cfg_signature : str
        The cryptographic signature (hex digest) provided for the file.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature matches; otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path and ensure file exists
    if not os.path.isfile(cfg_name):
        raise IOError(f"Configuration file '{cfg_name}' not found")

    try:
        with open(cfg_name, "rb") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    # Compute the SHA‑256 signature of the file content
    computed_sig = _compute_sha256(content)

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_sig, cfg_signature):
        return None

    # Optional: cross‑check against the global trusted signatures
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if trusted_sig and not hmac.compare_digest(trusted_sig, computed_sig):
        return None

    # Parse the configuration assuming JSON format
    try:
        config = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If parsing fails, treat as invalid
        return None

    return config