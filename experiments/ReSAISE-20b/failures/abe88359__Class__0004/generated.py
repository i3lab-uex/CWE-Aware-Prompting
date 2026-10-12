import os
import hashlib
import hmac

# Global mapping of filenames to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: 'config.json': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
}

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Verify the authenticity of a configuration file.

    Parameters
    ----------
    cfg_name : str
        The name (or path) of the configuration file to read.
    cfg_signature : str
        The cryptographic signature (hex digest) that the caller believes is correct.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches a trusted value,
        otherwise ``None``.
    Raises
    ------
    IOError
        If the configuration file cannot be located or opened.
    """
    # Resolve the absolute path for reproducibility
    cfg_path = os.path.abspath(cfg_name)

    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_path}' not found")

    # Compute the SHA‑256 digest of the file content
    sha256 = hashlib.sha256()
    try:
        with open(cfg_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{cfg_path}': {exc}") from exc

    computed_sig = sha256.hexdigest()

    # 1. Ensure the caller supplied signature matches the computed one
    if not hmac.compare_digest(computed_sig, cfg_signature):
        return None

    # 2. Ensure the computed signature is in the list of trusted signatures
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(os.path.basename(cfg_path))
    if not expected_sig or not hmac.compare_digest(computed_sig, expected_sig):
        return None

    # 3. Load the configuration (assuming JSON for this example)
    import json
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Configuration file is corrupted or not valid JSON
        return None

    return config