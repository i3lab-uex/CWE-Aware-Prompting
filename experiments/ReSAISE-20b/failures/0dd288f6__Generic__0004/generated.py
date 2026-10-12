import json
import hashlib
from pathlib import Path

# Example trusted signatures dictionary. In real usage this would be defined elsewhere.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "3b5d5c3712955042212316173ccf37be8009e4e2b4d1c5a8d7ef3f9b0c6a6e2b",
    # add more trusted signatures as needed
}

def apply_config_data(configuration_name: str, config_signature: str):
    """
    Read a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The filename of the configuration file to load.
    config_signature : str
        The expected cryptographic signature (hexadecimal string) for the file.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Resolve path (assume current working directory)
    config_path = Path(configuration_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found")

    # Read file content in binary mode
    try:
        with config_path.open("rb") as f:
            data_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{configuration_name}': {exc}") from exc

    # Compute SHA-256 hash of the file contents
    computed_hash = hashlib.sha256(data_bytes).hexdigest()

    # Verify signature matches expected value
    if computed_hash.lower() != config_signature.lower():
        return None

    # Parse JSON safely
    try:
        config_text = data_bytes.decode("utf-8")
        config_dict = json.loads(config_text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        # If the file is not valid JSON, treat it as invalid
        return None

    return config_dict