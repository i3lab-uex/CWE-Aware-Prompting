import json
import os
import hashlib
import hmac

# Example trusted signatures (filename -> expected SHA256 hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # add more trusted files here
}


def _compute_file_hash(file_path: str) -> str:
    """
    Compute the SHA256 hex digest of a file.
    """
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def handle_config_file(file_name: str, sign: str):
    """
    Read a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    sign : str
        Provided cryptographic signature (hex string).

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path (prevent directory traversal)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, file_name)

    if not os.path.isfile(file_path):
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Compute the hash of the actual file
    try:
        actual_hash = _compute_file_hash(file_path)
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{file_name}': {exc}") from exc

    # Verify the provided signature against the trusted one
    expected_hash = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if not expected_hash:
        # No trusted signature registered for this file
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE-693)
    if not hmac.compare_digest(actual_hash, sign):
        return None
    if not hmac.compare_digest(sign, expected_hash):
        return None

    # Parse JSON configuration
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        # If the file cannot be parsed, treat it as invalid
        return None

    return config