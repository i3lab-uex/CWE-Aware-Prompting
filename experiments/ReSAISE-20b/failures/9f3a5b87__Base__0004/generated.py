import os
import json
import hmac
import hashlib

# Example trusted signatures mapping (file name -> hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more trusted signatures here
}

def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file.
    file_signature : str
        Hex-encoded cryptographic signature sent with the data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Ensure the requested file exists
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Read the raw file content
    try:
        with open(file_name, "rb") as f:
            data_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{file_name}': {exc}") from exc

    # Compute the SHA-256 digest of the file contents
    computed_digest = hashlib.sha256(data_bytes).hexdigest()

    # Retrieve the expected signature for this file
    expected_digest = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_digest is None:
        # No trusted signature known for this file – treat as invalid
        return None

    # Use constant-time comparison to avoid timing attacks (CWE-347)
    if not hmac.compare_digest(computed_digest, expected_digest):
        return None

    # Parse the JSON configuration
    try:
        config_dict = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # Malformed JSON – treat as invalid
        return None

    return config_dict