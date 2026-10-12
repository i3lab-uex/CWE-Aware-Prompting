import os
import json
import hmac

# Global dictionary mapping filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real values
    "config1.json": "a3f9c2e4d8b7... (hex)",
    "config2.yaml": "5b1a9f4c3e2d... (hex)",
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    filename : str
        Name of the configuration file to read.
    cryptographic_signature : str
        Signature supplied alongside the configuration data (hex string).

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature matches a trusted value;
        otherwise, ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Resolve absolute path and ensure it is within allowed directory
    abs_path = os.path.abspath(filename)

    # Optional: enforce that the file is within a specific config directory
    # base_dir = os.path.abspath("/etc/myapp/config")
    # if not abs_path.startswith(base_dir):
    #     raise IOError(f"Access to {filename} is forbidden")

    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Load the trusted signature for this file, if any
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # No trusted signature known – treat as invalid
        return None

    # Compare signatures using constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(cryptographic_signature.lower(), expected_sig.lower()):
        return None

    # Read and parse the configuration file
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            # Support JSON; adapt if other formats are used
            config_data = json.load(f)
    except Exception as e:
        # If parsing fails, treat as invalid
        return None

    if not isinstance(config_data, dict):
        # Configuration must be a dictionary
        return None

    return config_data