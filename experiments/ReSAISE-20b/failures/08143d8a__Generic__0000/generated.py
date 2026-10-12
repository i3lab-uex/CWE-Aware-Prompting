import json
from pathlib import Path
from typing import Dict, Optional

# Global mapping of trusted signatures to the filenames they authorize.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries:
    # "a1b2c3d4e5f6g7h8i9j0": "config1.json",
    # "1234567890abcdef":       "config2.yaml",
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a configuration file and return its contents.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    provided_sig : str
        Cryptographic signature supplied alongside the config data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Validate signature against the trusted list
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if expected_file != config_filename:
        # Signature does not match the requested file
        return None

    # Resolve the path to the configuration file
    config_path = Path(config_filename)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' not found.")

    try:
        # Load the configuration data (assuming JSON format for safety)
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Wrap any I/O or parsing errors in an IOError for consistency
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    return data