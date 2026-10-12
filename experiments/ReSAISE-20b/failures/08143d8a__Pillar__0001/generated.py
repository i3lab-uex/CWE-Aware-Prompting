import json
import os
import hmac
from pathlib import Path

# Global dictionary mapping valid cryptographic signatures to configuration filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real signatures in production
    "a1b2c3d4e5f6g7h8i9j0": "config1.json",
    "1234567890abcdef":     "config2.yaml",
}

def _is_trusted_signature(provided_sig: str, expected_filename: str) -> bool:
    """
    Compare the provided signature against the trusted signature for the
    expected configuration file in a timing‑attack resistant manner.
    """
    # Retrieve the trusted signature for this filename, if any
    trusted_sig = None
    for sig, fname in TRUSTED_CONFIG_SIGNATURES.items():
        if fname == expected_filename:
            trusted_sig = sig
            break

    # If no trusted signature exists for this file, authentication fails.
    if trusted_sig is None:
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(provided_sig, trusted_sig)

def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Reads a configuration file after validating its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    provided_sig : str
        Cryptographic signature supplied alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be accessed.
    """
    # Prevent directory traversal attacks by only allowing a single component name
    safe_name = os.path.basename(config_filename)

    # Resolve the absolute path of the configuration file
    config_path = Path(safe_name).resolve()

    # Ensure the file exists and is a regular file
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' not found.")

    # Verify the provided signature
    if not _is_trusted_signature(provided_sig, safe_name):
        # Signature mismatch – do not expose any configuration data
        return None

    # Read and parse the configuration file (assuming JSON for simplicity)
    try:
        with config_path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:
        # Propagate any I/O or JSON parsing errors
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    return data