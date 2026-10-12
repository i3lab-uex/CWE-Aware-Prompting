import json
import os

# Global mapping of configuration file names to their trusted cryptographic signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (replace with actual trusted signatures)
    "app_settings.json": "d2c3e1f4a5b6c7d8e9f0",
    "database_config.json": "a1b2c3d4e5f6g7h8i9j0",
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        Name of the configuration file to load (e.g., "app_settings.json").
    signature : str
        Cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid.
        Returns ``None`` if the signature does not match or the file contains
        invalid JSON.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Verify that we have a trusted signature for this configuration
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if expected_sig is None or signature != expected_sig:
        # Signature missing or does not match
        return None

    # Resolve the absolute path to avoid directory traversal attacks
    config_path = os.path.abspath(config_name)

    # Ensure the file is within an allowed directory (e.g., current working dir)
    if not config_path.startswith(os.getcwd()):
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        # Re‑raise as IOError to match the specification
        raise IOError(f"Configuration file '{config_name}' not found") from e
    except json.JSONDecodeError:
        # Invalid JSON content; treat as untrusted
        return None

    # Optionally, further validate the structure of `data` here.
    return data