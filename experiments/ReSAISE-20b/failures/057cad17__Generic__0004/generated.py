import os
import json

# Global mapping of trusted signatures to configuration file names.
# In a real system this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: 'abc123signature': 'config.json',
}

def handle_config_file(filename: str, sig: str):
    """
    Load a configuration file only if the provided cryptographic signature
    is trusted for that filename.

    Parameters:
        filename (str): The name of the configuration file to load.
        sig (str):   A cryptographic signature that must be verified.

    Returns:
        dict: The parsed configuration data if the signature is valid.
        None: If the signature does not match the trusted mapping.

    Raises:
        IOError: If the requested configuration file cannot be found or read.
    """
    # Ensure we are only dealing with a single path component to avoid
    # directory traversal attacks.
    if os.path.sep in filename or os.path.altsep and os.path.altsep in filename:
        raise ValueError("Invalid configuration file name")

    # Verify that the signature is trusted for this filename
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        return None

    # Resolve the absolute path of the configuration file
    config_path = os.path.abspath(filename)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{filename}' not found")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            # Assuming the configuration file is JSON; adjust if needed.
            config_data = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers file I/O errors; ValueError covers JSON decoding errors.
        raise IOError(f"Failed to read configuration file '{filename}': {exc}") from exc

    return config_data