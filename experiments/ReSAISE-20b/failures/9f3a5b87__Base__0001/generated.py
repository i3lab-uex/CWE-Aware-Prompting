import os
import json
import hashlib
import hmac

# Global dictionary mapping filenames to their expected SHA256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (to be filled with real values)
    # "config.yaml": "3a7bd3e2360f... (hex signature)",
    # "settings.json": "b5c1d2e3f4a... (hex signature)",
}

def handle_config_data(file_name: str, file_signature: str) -> dict | None:
    """
    Retrieve configuration data from *file_name*, verify its cryptographic
    signature against the trusted list and return it as a dictionary.
    
    Parameters:
        file_name (str): Name of the configuration file to read.
        file_signature (str): Cryptographic signature provided with the file.
    
    Returns:
        dict | None: Parsed configuration data if the signature is valid;
                     otherwise, None.
    
    Raises:
        IOError: If *file_name* does not exist or cannot be read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Read the entire content in binary mode
    try:
        with open(file_name, "rb") as f:
            content = f.read()
    except OSError as exc:  # Covers permission errors, etc.
        raise IOError(f"Unable to read configuration file '{file_name}': {exc}") from exc

    # Compute SHA256 digest of the content
    computed_digest = hashlib.sha256(content).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_digest, file_signature):
        # Signature mismatch; do not trust the data
        return None

    # Optionally, verify that the file is listed in the trusted signatures
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig and not hmac.compare_digest(expected_sig, file_signature):
        # The signature is valid but does not match the expected trusted one
        return None

    # Parse JSON configuration; raise if malformed
    try:
        config = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # Malformed or non‑JSON content; treat as invalid
        raise IOError(f"Configuration file '{file_name}' contains invalid JSON: {exc}") from exc

    if not isinstance(config, dict):
        # Expect a dictionary at the top level
        raise IOError(f"Configuration file '{file_name}' does not contain a JSON object")

    return config