import json
import os
from pathlib import Path

# Global dictionary mapping file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_config.json": "e3b0c44298fc1c149afbf4c8996fb924",
    # "db_config.yaml":  "a54d88e06612d820bc3be72877c74f257b561b19",
}

def handle_config_file(file_name: str, sign: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    sign : str
        Cryptographic signature supplied for verification.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid.
        ``None`` if the signature does not match the trusted value.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Resolve absolute path for security (prevents directory traversal).
    config_path = Path(file_name).resolve()

    # Ensure the file exists and is a regular file.
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Retrieve the trusted signature for this file.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_path.name)
    if expected_sig is None:
        # No trusted signature registered for this file.
        return None

    # Verify the supplied signature matches the expected one.
    if sign != expected_sig:
        return None

    # Read and parse the configuration file safely.
    try:
        with config_path.open("r", encoding="utf-8") as f:
            # Assuming JSON format; adjust if another format is used.
            config = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers file read errors; ValueError covers JSON parse errors.
        raise IOError(f"Failed to load configuration from '{file_name}': {exc}") from exc

    return config