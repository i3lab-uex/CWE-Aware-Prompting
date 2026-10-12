import json
from pathlib import Path

# Global dictionary mapping valid signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (signature : filename)
    # "a1b2c3d4e5f6g7h8i9j0": "app_config.json",
    # "1234567890abcdef1234": "db_settings.json",
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Load a configuration file only if the supplied signature matches an entry
    in TRUSTED_CONFIG_SIGNATURES for that filename.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to load.
    provided_sig : str
        Cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the signature matches the expected value for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None or provided_sig != expected_sig:
        # Invalid signature – do not load the file
        return None

    # Resolve the path to prevent directory traversal attacks
    config_path = Path(config_filename).resolve()
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' not found")

    # Read and parse the configuration file
    try:
        with config_path.open("r", encoding="utf-8") as f:
            # Assuming JSON configuration; adjust if needed
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # Log the error or re-raise with a more descriptive message
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    return config_data