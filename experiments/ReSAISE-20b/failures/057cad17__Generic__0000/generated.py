import json
import os

# Example trusted signatures mapping.
# In practice this should be securely populated from a trusted source.
TRUSTED_CONFIG_SIGNATURES = {
    # signature: filename
    "abc123def456": "app_config.json",
    "789ghi012jkl": "db_settings.yaml",  # Example for YAML support if needed
}

def handle_config_file(filename: str, sig: str):
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    filename : str
        The name of the configuration file to load.
    sig : str
        The cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Verify that the provided signature is trusted for this filename
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Signature does not match the requested file
        return None

    # Resolve absolute path to prevent directory traversal attacks
    safe_path = os.path.abspath(filename)
    if not os.path.isfile(safe_path):
        raise IOError(f"Configuration file '{filename}' not found.")

    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            # Attempt to parse JSON; extendable for other formats
            return json.load(f)
    except Exception as exc:
        # Wrap any file read/parse error in an IOError for consistency
        raise IOError(f"Failed to load configuration '{filename}': {exc}") from exc