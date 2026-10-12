import json
from pathlib import Path
from typing import Dict, Optional

# Example trusted signatures mapping (should be populated elsewhere in the real application)
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config.json": "sha256-hash-of-config",
}

def retrieve_config_data(config_filename: str, crypt_signature: str) -> Optional[Dict]:
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        The name of the configuration file to load.
    crypt_signature : str
        The cryptographic signature provided alongside the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Resolve the path safely
    config_path = Path(config_filename).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Load the file contents securely
    try:
        with config_path.open("r", encoding="utf-8") as f:
            raw_data = f.read()
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    # Verify the signature
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_path.name)
    if expected_signature is None or expected_signature != crypt_signature:
        return None

    # Parse JSON safely
    try:
        config_dict = json.loads(raw_data)
    except json.JSONDecodeError:  # pragma: no cover
        return None

    if not isinstance(config_dict, dict):
        return None

    return config_dict