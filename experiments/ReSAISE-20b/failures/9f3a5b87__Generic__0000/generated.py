import json
from pathlib import Path
from typing import Dict, Optional

# Example trusted signatures mapping.
# In a real system this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "app_config.json": "d2c3e5a1f4b9a0c6",
    # Add more trusted filenames and their signatures here.
}


def handle_config_data(file_name: str, file_signature: str) -> Optional[Dict]:
    """
    Retrieve configuration data from a JSON file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file.
    file_signature : str
        Cryptographic signature provided alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Resolve the path to prevent directory traversal attacks
    config_path = Path(file_name).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Verify that the supplied signature matches the trusted one
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_path.name)
    if expected_sig is None or expected_sig != file_signature:
        # Signature mismatch – reject the data
        return None

    # Read and parse JSON safely
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Malformed JSON – treat as invalid
        return None

    if not isinstance(data, dict):
        # The configuration must be a dictionary
        return None

    return data