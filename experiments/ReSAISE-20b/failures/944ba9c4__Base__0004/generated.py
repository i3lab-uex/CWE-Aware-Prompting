import os
import json
import hmac

# Global mapping of trusted configuration files to their expected signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example:
    # "config.json": "5f2c3d4e6a7b8c9d0e1f2g3h4i5j6k7l",
}

def validate_config_file(filename: str, cryptographic_signature: str) -> dict | None:
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    filename : str
        Path to the configuration file.
    cryptographic_signature : str
        Signature claimed for the contents of ``filename``.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches; otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Load the expected signature from the trusted list
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # If the file is not in the trusted list, treat it as untrusted
        return None

    # Read the file contents (bytes for accurate signature comparison)
    try:
        with open(filename, "rb") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{filename}': {exc}") from exc

    # Perform a constant‑time comparison of the provided and expected signatures
    if not hmac.compare_digest(cryptographic_signature, expected_sig):
        return None

    # Parse the configuration assuming JSON format
    try:
        config = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If the file contents are not valid JSON, consider it invalid
        return None

    if not isinstance(config, dict):
        # Configuration must be a dictionary
        return None

    return config