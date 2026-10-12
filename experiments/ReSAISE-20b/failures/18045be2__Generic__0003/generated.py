import json
import os

# Example global dictionary mapping valid signatures to configuration filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # "signature_string": "config_file_name.json",
}

def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Retrieve and verify a configuration file against its cryptographic signature.

    Parameters
    ----------
    config_file : str
        The name of the configuration file to load.
    provided_signature : str
        The cryptographic signature accompanying the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or read.
    """
    # Ensure that the provided signature is actually associated with this file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if expected_file != config_file:
        return None  # signature does not match the requested file

    # Resolve a safe absolute path (prevent directory traversal)
    base_dir = os.path.abspath(".")          # change as appropriate
    safe_path = os.path.normpath(os.path.join(base_dir, config_file))
    if not safe_path.startswith(base_dir):
        raise IOError(f"Unsafe file path: {config_file}")

    # Read and parse the configuration file
    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        raise IOError(f"Configuration file not found: {config_file}")
    except json.JSONDecodeError as e:
        raise IOError(f"Invalid JSON in configuration file '{config_file}': {e}")

    return config_data