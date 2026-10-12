import json
import os
from pathlib import Path
import hmac

# Global dictionary mapping valid signatures to config filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (signature : filename)
    # "e3b0c442...": "default.conf",
}

def _is_path_safe(config_filename: str) -> bool:
    """
    Ensure the supplied filename does not contain any directory traversal
    characters. Only allow a simple base name.
    """
    # Reject absolute paths or any path separators
    return not (os.path.isabs(config_filename) or '/' in config_filename or '\\' in config_filename)

def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Read a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    provided_sig : str
        Cryptographic signature supplied alongside the config data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid; otherwise,
        None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # 1. Basic sanity checks
    if not _is_path_safe(config_filename):
        raise IOError(f"Unsafe configuration filename: {config_filename}")

    config_path = Path(config_filename)

    # 2. Ensure file exists and is readable
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' not found")

    try:
        content_bytes = config_path.read_bytes()
    except OSError as exc:  # pragma: no cover
        raise IOError(f"Error reading configuration file '{config_filename}': {exc}") from exc

    # 3. Verify the signature
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # No trusted signature known for this file
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693)
    if not hmac.compare_digest(provided_sig, expected_sig):
        return None

    # 4. Parse configuration (assuming JSON; adjust as needed)
    try:
        config_text = content_bytes.decode('utf-8')
        return json.loads(config_text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:  # pragma: no cover
        raise IOError(f"Failed to parse configuration file '{config_filename}': {exc}") from exc