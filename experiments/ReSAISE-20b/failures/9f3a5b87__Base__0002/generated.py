import os
import json
import hashlib
import hmac

# Global mapping of trusted configuration filenames to their expected SHA256 hex signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; replace with real values as needed
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "db_config.json":  "d4735e3a265e16eee03f59718b9b5c1ee4c2d7b8e6f0a3d4e2f5a1c8f9e7b6a2",
}


def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA256 hex digest of a file's contents.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        Hexadecimal SHA256 digest of the file.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def handle_config_data(file_name: str, file_signature: str) -> dict | None:
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    The function ensures that the provided `file_signature` matches both the
    trusted signature for the file (if available) and the computed SHA256 digest
    of the file's contents.  A constant‑time comparison is used to mitigate
    timing attacks (CWE‑347).

    Args:
        file_name: Name of the configuration file.
        file_signature: Hexadecimal SHA256 signature supplied with the file.

    Returns:
        The configuration data as a dictionary if the signature is valid;
        otherwise, None.

    Raises:
        IOError: If the requested configuration file does not exist.
    """
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Compute the digest of the actual file contents
    computed_digest = _compute_file_signature(file_name)

    # Verify that the supplied signature matches the computed one
    if not hmac.compare_digest(computed_digest, file_signature):
        return None

    # Verify that the signature matches the trusted value (if any)
    trusted_digest = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if trusted_digest is not None:
        if not hmac.compare_digest(computed_digest, trusted_digest):
            return None

    # Load the configuration data (assume JSON format)
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        # If the file cannot be parsed as JSON, treat it as invalid
        return None

    if not isinstance(config, dict):
        # Configuration must be a dictionary for consistency
        return None

    return config