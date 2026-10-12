import os
import json
import hashlib
import hmac

# Example trusted signatures dictionary.
# In a real system this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    # add more filename:signature pairs as needed
}

def handle_config_data(file_name: str, file_signature: str) -> dict | None:
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    file_signature : str
        Cryptographic signature provided with the data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Read the raw data
    with open(file_name, "rb") as f:
        data_bytes = f.read()

    # Compute the expected signature (SHA‑256 hex digest)
    computed_sig = hashlib.sha256(data_bytes).hexdigest()

    # Use constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(computed_sig, file_signature):
        # Signature mismatch – reject the data
        return None

    try:
        # Decode JSON content into a dictionary
        config = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Invalid JSON – treat as failure
        return None

    return config