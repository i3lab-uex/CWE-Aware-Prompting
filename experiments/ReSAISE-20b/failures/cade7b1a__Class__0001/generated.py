import json
import os
import hashlib
import hmac

# Global mapping of configuration file names to their trusted SHA‑256 signatures (hex strings)
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; populate with actual values
    "app_config.json": "5f2c3e8b9d1a4f6b7c0e2d1f4a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4g5",
    "db_config.json":  "9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3q2r1s0t9u8v7w6x5y4z3a2b1c0d9e8f",
    # Add more trusted signatures here
}

def _compute_sha256(data: bytes) -> str:
    """Return the hex digest of SHA‑256 over *data*."""
    return hashlib.sha256(data).hexdigest()

def process_config_data(config_name: str, signature: str):
    """
    Load a configuration file and verify its integrity.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load (relative to the current working directory).
    signature : str
        The cryptographic signature provided for this configuration.  It must match the SHA‑256
        hash of the file contents.

    Returns
    -------
    dict | None
        The parsed configuration data if the signature is valid; otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve the absolute path and ensure the file exists
    config_path = os.path.abspath(config_name)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Read the raw bytes of the configuration file
    try:
        with open(config_path, "rb") as f:
            raw_data = f.read()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{config_name}': {exc}") from exc

    # Compute the SHA‑256 hash of the file content
    computed_sig = _compute_sha256(raw_data)

    # Compare the provided signature with the trusted one
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not trusted_sig:
        # No trusted signature known for this file – reject it
        return None

    # Use timing‑safe comparison to mitigate side‑channel attacks
    if not hmac.compare_digest(computed_sig, trusted_sig):
        # Signature mismatch – data authenticity cannot be guaranteed
        return None

    # Verify that the provided signature matches the computed one (redundant but defensive)
    if not hmac.compare_digest(computed_sig, signature):
        return None

    # Parse the configuration as JSON
    try:
        config_dict = json.loads(raw_data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Malformed configuration – treat as invalid
        return None

    return config_dict