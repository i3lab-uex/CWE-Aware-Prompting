import json
from pathlib import Path

# Global dictionary mapping file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (to be populated elsewhere in the application)
    # 'config.json': 'abcd1234efgh5678',
}

def handle_config_file(file_name: str, sign: str):
    """
    Read and validate a configuration file.

    Parameters
    ----------
    file_name : str
        The name of the configuration file to read.
    sign : str
        The cryptographic signature supplied for this configuration.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature matches a trusted one;
        otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Resolve the path to avoid relative traversal attacks
    config_path = Path(file_name).resolve()

    # Verify the file exists and is a regular file
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Verify that the supplied signature matches the trusted one
    expected_sign = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sign is None:
        # No trusted signature available for this file
        return None

    if sign != expected_sign:
        # Signature mismatch – reject the configuration
        return None

    try:
        with config_path.open("r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Any I/O or parsing error is treated as a fatal issue
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc

    # Ensure the parsed data is a dictionary
    if not isinstance(config_data, dict):
        raise ValueError(f"Configuration file '{file_name}' does not contain a JSON object.")

    return config_data