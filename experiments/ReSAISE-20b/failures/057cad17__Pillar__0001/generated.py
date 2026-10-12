import os
from typing import Dict, Optional

# Global dictionary mapping valid signatures to file names.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real signatures and file names.
    "abc123def456": "app_config.json",
    "789ghi012jkl": "db_settings.yaml",
}

def handle_config_file(filename: str, sig: str) -> Optional[Dict]:
    """
    Read a configuration file only if its signature is trusted.

    Parameters
    ----------
    filename : str
        Name of the configuration file to load.
    sig : str
        Cryptographic signature supplied for the configuration.

    Returns
    -------
    dict | None
        Parsed configuration data if signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be opened.
    """
    # 1. Validate signature against trusted mapping
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Signature does not match the file; reject.
        return None

    # 2. Attempt to read the file
    try:
        with open(filename, "rb") as f:
            data = f.read()
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{filename}' not found") from exc
    except OSError as exc:
        # Other I/O errors (permissions, etc.)
        raise IOError(f"Error reading configuration file '{filename}': {exc}") from exc

    # 3. Safely parse the configuration data.
    #    Assume JSON for this example; adjust if another format is used.
    try:
        import json
        config = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed data – treat as invalid
        return None

    # 4. Return the parsed configuration dictionary.
    return config