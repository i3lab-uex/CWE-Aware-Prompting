import json
import os
import hmac

# Example trusted signatures dictionary. In a real system this would be securely stored.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
    # Add more trusted filenames and their signatures here
}


def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        The name of the file containing the configuration data.
    crypt_signature : str
        The cryptographic signature sent with the configuration data.

    Returns
    -------
    dict | None
        The configuration data as a dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Load the trusted signature for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # No trusted signature registered for this file; treat as invalid
        return None

    # Perform a constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(crypt_signature, expected_sig):
        # Signature mismatch – reject the file
        return None

    # Read and parse the configuration file safely
    try:
        with open(config_filename, "r", encoding="utf-8") as fp:
            config_data = json.load(fp)
    except (json.JSONDecodeError, OSError) as exc:
        # Treat parsing errors or read errors as a failure to retrieve valid data
        return None

    if not isinstance(config_data, dict):
        # Unexpected format – reject the data
        return None

    return config_data