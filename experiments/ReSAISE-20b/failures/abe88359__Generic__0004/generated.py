import json
import os
import hashlib
import hmac

# Global dictionary mapping filenames to their expected signatures (hex strings)
TRUSTED_CONFIG_SIGNATURES = {
    # Example:
    # "app_config.json": "a1b2c3d4e5f6...",
}

def _compute_signature(data: bytes) -> str:
    """
    Compute the SHA256 hex digest of the given data.
    """
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Verify that the configuration file `cfg_name` exists, its SHA256 signature
    matches both the provided `cfg_signature` and the trusted value in
    TRUSTED_CONFIG_SIGNATURES. If valid, return the parsed JSON configuration.
    Return None if the signature does not match.

    Raises:
        IOError: If the file cannot be located or read.
    """
    # Resolve absolute path (no relative traversal allowed)
    cfg_path = os.path.abspath(cfg_name)

    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_name}' not found")

    try:
        with open(cfg_path, "rb") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Could not read configuration file '{cfg_name}': {exc}") from exc

    # Compute the signature of the file content
    computed_sig = _compute_signature(content)

    # Compare with provided signature (constant‑time)
    if not hmac.compare_digest(computed_sig, cfg_signature):
        return None

    # Compare with the trusted signature if available
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if expected_sig is not None and not hmac.compare_digest(computed_sig, expected_sig):
        return None

    # Parse the JSON configuration
    try:
        config = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise IOError(f"Invalid JSON in configuration file '{cfg_name}': {exc}") from exc

    return config