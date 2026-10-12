import json
import os

# Global dictionary mapping cryptographic signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real signatures and filenames
    "a1b2c3d4e5f6g7h8i9j0": "app_config.json",
    "z9y8x7w6v5u4t3s2r1q0": "db_config.json",
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Validate a configuration file against its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to load.
    provided_sig : str
        Cryptographic signature that should match the trusted mapping.

    Returns
    -------
    dict | None
        Parsed configuration data if signature is valid, otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # 1. Verify that the provided signature is known and maps to the requested file.
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if expected_file != config_filename:
        # Signature does not match the requested file – refuse to load.
        return None

    # 2. Resolve absolute path (optional, but prevents relative traversal attacks).
    config_path = os.path.abspath(config_filename)

    # 3. Ensure the file exists and is readable.
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_filename}' not found.")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            # 4. Parse JSON configuration.
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Wrap any I/O or JSON parsing errors in an IOError.
        raise IOError(f"Failed to load configuration file '{config_filename}': {exc}") from exc

    # 5. Return the parsed configuration dictionary.
    return config_data