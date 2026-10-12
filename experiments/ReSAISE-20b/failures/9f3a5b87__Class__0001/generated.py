import json
import os

# Example trusted signatures dictionary.
# In a real application this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES = {
    "config.json": "a1b2c3d4e5f6g7h8i9j0",
    # Add other trusted file signatures here.
}


def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from *file_name* and verify that the provided
    *file_signature* matches the trusted signature for this file.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    file_signature : str
        Cryptographic signature supplied by the caller.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Verify that the supplied signature matches the trusted value
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_signature is None:
        # No trusted signature known for this file – reject it
        return None

    if file_signature != expected_signature:
        # Signature mismatch – data authenticity cannot be guaranteed
        return None

    # Read and parse the configuration file safely
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            config_text = f.read()
        # Use json.loads to parse the configuration into a dictionary
        config_data = json.loads(config_text)
    except (OSError, json.JSONDecodeError) as exc:
        # Propagate file I/O errors and JSON parsing issues
        raise IOError(f"Failed to read or parse configuration: {exc}") from exc

    # Ensure the resulting data is a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data