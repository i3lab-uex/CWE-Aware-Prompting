import json
import os
import hashlib
import hmac

# Global mapping of config file names to their trusted SHA-256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – in real usage these would be populated with actual values.
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "db_config.json":  "9e107d9d372bb6826bd81d3542a419d6c8b0e3f3d4a9c9ea1e5c4c3d2b0f1234",
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA-256 hex digest of a file's contents.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its authenticity.

    Parameters
    ----------
    config_name : str
        Name of the configuration file to load.
    signature : str
        Cryptographic signature (hex SHA-256 digest) provided alongside the config data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature matches the trusted value;
        otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path – prevent directory traversal attacks
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, config_name)

    if not os.path.isfile(file_path):
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Compute the actual signature of the file
    try:
        computed_sig = _compute_file_signature(file_path)
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{config_name}': {exc}") from exc

    # Ensure the provided signature matches the trusted one
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not expected_sig:
        # No trusted signature known for this file – reject
        return None

    if not hmac.compare_digest(computed_sig, expected_sig):
        # Signature mismatch – data authenticity cannot be guaranteed
        return None

    if not hmac.compare_digest(computed_sig, signature):
        # The supplied signature does not match the file – treat as invalid
        return None

    # All checks passed; load and return configuration data
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        raise IOError(f"Failed to parse configuration file '{config_name}': {exc}") from exc