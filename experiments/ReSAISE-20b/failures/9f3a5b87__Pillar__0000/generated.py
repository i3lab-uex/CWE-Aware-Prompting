import json
from pathlib import Path
import hmac

# Global dictionary mapping filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with actual values in production
    "config.yaml": "abc123def456...",
    "settings.json": "789xyz012mno..."
}

def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from *file_name* and verify its cryptographic
    signature against the trusted signatures.

    Parameters:
        file_name (str): Name of the configuration file.
        file_signature (str): Signature supplied alongside the file.

    Returns:
        dict: Parsed configuration data if signature is valid.
        None: If the signature does not match or file contents cannot be parsed.

    Raises:
        IOError: If the requested configuration file does not exist.
    """
    # Resolve to an absolute path; this can be tightened to a specific directory if needed.
    file_path = Path(file_name).resolve()

    # Ensure the file exists before attempting to read it.
    if not file_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Retrieve the trusted signature for this filename, if any.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_path.name)
    if expected_sig is None:
        # No trusted signature known – treat as invalid.
        return None

    # Perform a constant‑time comparison to avoid timing attacks (CWE-693).
    if not hmac.compare_digest(file_signature, expected_sig):
        return None

    # Read and parse the file contents.
    try:
        with file_path.open("r", encoding="utf-8") as f:
            # Support JSON; adapt if another format is required.
            data = json.load(f)
    except (OSError, ValueError):
        # OSError covers file read errors; ValueError covers JSON decoding issues.
        return None

    if not isinstance(data, dict):
        # Expecting a dictionary; otherwise the config is malformed.
        return None

    return data