import json
from pathlib import Path

# Global mapping of valid signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "abcd1234efgh5678": "config1.json",
    # "ijkl9012mnop3456": "config2.yaml",
}

def handle_config_file(filename: str, sig: str) -> dict | None:
    """
    Retrieve and validate a configuration file.

    Parameters
    ----------
    filename : str
        Name of the configuration file to retrieve.
    sig : str
        Cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        Dictionary containing the configuration data if the signature is valid.
        Returns ``None`` if the signature does not match the expected value.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Verify that the provided signature is trusted and corresponds to this file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Signature is invalid or does not match the requested file
        return None

    config_path = Path(filename)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{filename}' is not available.")

    try:
        with config_path.open("r", encoding="utf-8") as f:
            # Attempt to parse the file as JSON.  If parsing fails,
            # treat it as a malformed configuration and raise an IOError.
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to read or parse configuration file '{filename}': {exc}") from exc

    return config_data