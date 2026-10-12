import json
import os
import hmac

# Global dictionary mapping valid signatures to config filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: "signature_value": "config.json",
    # Populate with real signatures in production.
}

def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to avoid timing attacks.
    """
    return hmac.compare_digest(a.encode(), b.encode())

def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Retrieve and verify a configuration file.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to retrieve.
    provided_sig : str
        Cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict or None
        Parsed JSON content if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Verify that the provided signature is expected for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if not expected_sig or not _constant_time_compare(provided_sig, expected_sig):
        # Signature mismatch or not trusted
        return None

    # Resolve the absolute path to prevent directory traversal attacks.
    base_dir = os.path.abspath(".")  # Adjust as needed
    safe_path = os.path.normpath(os.path.join(base_dir, config_filename))

    # Ensure the file resides within the base directory
    if not safe_path.startswith(base_dir):
        raise IOError("Invalid configuration file path")

    # Read the file contents
    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{config_filename}' not found") from exc

    # Parse JSON safely
    try:
        config_data = json.loads(content)
    except json.JSONDecodeError as exc:
        # Corrupt or invalid JSON; treat as untrusted
        return None

    return config_data