import json
from pathlib import Path

# Example trusted signatures dictionary. In real usage this should be populated securely.
TRUSTED_CONFIG_SIGNATURES = {
    "config.yaml": "d41d8cd98f00b204e9800998ecf8427e",
    "settings.json": "0cc175b9c0f1b6a831c399e269772661",
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from an external file and verify its
    cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Cryptographic signature that should match the trusted one.

    Returns
    -------
    dict | None
        The configuration data if the signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be opened.
    """
    # Resolve the absolute path to guard against relative path traversal
    file_path = Path(config_filename).resolve()

    # Verify that the file exists and is a regular file
    if not file_path.is_file():
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Verify the signature against the trusted dictionary
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_path.name)
    if expected_sig is None or expected_sig.lower() != crypt_signature.lower():
        # Signature mismatch – do not load the data
        return None

    try:
        with file_path.open("r", encoding="utf-8") as f:
            # Assuming JSON format; adjust if a different format is used
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Re-raise as IOError to match the specification
        raise IOError(f"Failed to read or parse configuration file '{config_filename}': {exc}")

    return config_data