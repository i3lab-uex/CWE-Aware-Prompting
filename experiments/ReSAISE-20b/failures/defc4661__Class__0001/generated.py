import json
import os
import hashlib
import hmac

# Example global dictionary mapping filenames to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # "config.json": "5f4dcc3b5aa765d61d8327deb882cf99..."
}

def _compute_file_signature(path: str) -> str:
    """Return the SHA‑256 hex digest of the file at *path*."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def handle_config_file(file_name: str, sign: str) -> dict | None:
    """
    Read a configuration file and verify its authenticity.

    Parameters
    ----------
    file_name : str
        Name (or relative path) of the configuration file to load.
    sign : str
        The cryptographic signature supplied by the caller, expected to be a
        hex‑encoded SHA‑256 digest.

    Returns
    -------
    dict | None
        Parsed JSON configuration if the signature matches; otherwise `None`.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Resolve absolute path to guard against directory traversal attacks
    abs_path = os.path.abspath(file_name)

    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{file_name}' not found")

    # Compute the signature of the actual file contents
    computed_sig = _compute_file_signature(abs_path)

    # Retrieve the trusted signature for this file (if any)
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)

    # Verify that the supplied signature matches both the computed and
    # trusted signatures using constant‑time comparison to mitigate timing attacks.
    if not (trusted_sig and
            hmac.compare_digest(computed_sig, trusted_sig) and
            hmac.compare_digest(sign.lower(), computed_sig)):
        return None

    # Load and parse the configuration (JSON expected)
    with open(abs_path, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            # Malformed JSON is considered a failure to verify authenticity
            return None

    if not isinstance(config, dict):
        # Expecting a dictionary; any other type is considered invalid
        return None

    return config