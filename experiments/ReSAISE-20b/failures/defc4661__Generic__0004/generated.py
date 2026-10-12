import os
import json
import hmac

# Example trusted signatures dictionary (to be populated elsewhere in the application)
TRUSTED_CONFIG_SIGNATURES = {
    # 'config.json': 'expected_signature_string',
}

def handle_config_file(file_name: str, sign: str):
    """
    Load a configuration file and verify its signature.

    Parameters
    ----------
    file_name : str
        Path to the configuration file.
    sign : str
        Signature string that should match the trusted signature for this file.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature matches.
        ``None`` if the signature does not match.

    Raises
    ------
    IOError
        If the file cannot be found or read.
    """
    # Resolve absolute path to prevent directory traversal issues
    abs_path = os.path.abspath(file_name)

    # Verify the file exists before attempting to open it
    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{file_name}' not found")

    # Retrieve the expected signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(os.path.basename(file_name))
    if expected_sig is None:
        # No trusted signature available; treat as untrusted
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sign, expected_sig):
        return None

    # Read and parse the configuration file
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers file read errors; ValueError covers JSON parsing errors
        raise IOError(f"Failed to load configuration from '{file_name}': {exc}") from exc

    return config