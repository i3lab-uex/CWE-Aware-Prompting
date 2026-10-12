import json
from pathlib import Path

# Global mapping of trusted signatures to allowed configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "abcdef1234567890": "app_config.json",
    # "fedcba0987654321": "db_config.json",
}

def handle_config_file(filename: str, sig: str):
    """
    Reads a configuration file after validating its cryptographic signature.

    Parameters
    ----------
    filename : str
        The name of the configuration file to load.
    sig : str
        The cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or read.
    """
    # Ensure that the signature is associated with this filename
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Signature does not match the requested file
        return None

    config_path = Path(filename)

    # Prevent path traversal attacks by resolving the absolute path
    try:
        config_path = config_path.resolve(strict=True)
    except FileNotFoundError as e:
        raise IOError(f"Configuration file '{filename}' not found.") from e

    # Read and parse the configuration file
    try:
        with config_path.open("r", encoding="utf-8") as f:
            # Assuming JSON configuration; adjust parsing if needed
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise IOError(f"Failed to read or parse configuration file '{filename}'.") from e

    return config_data