import os
import json
import hmac

# Global dictionary mapping filenames to their trusted cryptographic signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real values in production
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more trusted config files and their SHA‑256 hex digests here.
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from *filename* and verify that the supplied
    cryptographic signature matches the trusted one stored in
    TRUSTED_CONFIG_SIGNATURES.

    Parameters:
        filename (str): Name of the configuration file.
        cryptographic_signature (str): Signature provided with the config data.

    Returns:
        dict: Parsed configuration data if signature is valid.
        None: If the signature does not match.

    Raises:
        IOError: If *filename* does not exist or cannot be read.
    """
    # 1. Ensure the file exists and is readable
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # 2. Compute the expected signature from the trusted dictionary
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_signature is None:
        # No trusted signature registered for this file – treat as invalid
        return None

    # 3. Compare signatures in constant time to avoid timing attacks
    if not hmac.compare_digest(
        cryptographic_signature.lower(), expected_signature.lower()
    ):
        return None

    # 4. Read and parse the configuration file (JSON format assumed)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers file read errors; ValueError covers JSON decode errors
        raise IOError(f"Failed to load configuration from '{filename}': {exc}") from exc

    # 5. Return the parsed configuration
    return config_data