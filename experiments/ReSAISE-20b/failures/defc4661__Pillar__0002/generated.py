import os
import hashlib
import hmac

# Global mapping of filenames to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: 'config.json': 'a3f5e1c...'
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA‑256 signature of a file in a memory‑efficient way.
    Returns the hexadecimal digest string.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def handle_config_file(file_name: str, sign: str) -> dict | None:
    """
    Read a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name (or relative path) of the configuration file.
    sign : str
        The cryptographic signature supplied for validation.  It should be a
        hexadecimal string representing the expected SHA‑256 digest.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches the
        trusted value; otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Resolve absolute path to avoid directory traversal attacks
    abs_path = os.path.abspath(file_name)

    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{file_name}' not found")

    # Compute the actual signature
    try:
        actual_sig = _compute_file_signature(abs_path)
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig is None:
        # No trusted signature available – treat as invalid
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE‑693)
    if not hmac.compare_digest(actual_sig, expected_sig):
        return None

    # If signature matches, read and parse the configuration
    try:
        import json
        with open(abs_path, "r", encoding="utf-8") as fh:
            config = json.load(fh)
    except Exception as exc:  # pragma: no cover
        # If parsing fails, treat as invalid but do not expose internals
        return None

    if not isinstance(config, dict):
        # Unexpected format – reject
        return None

    return config