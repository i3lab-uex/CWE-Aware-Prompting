import json
import os
import hmac

# Global dictionary mapping configuration filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; replace with actual values in production
    "app_settings.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "db_config.json":   "5d41402abc4b2a76b9719d911017c592",
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load.
    signature : str
        The cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration data if the signature is valid; otherwise `None`.

    Raises
    ------
    IOError
        If the configuration file cannot be found or is unreadable.
    """
    # Resolve the absolute path to prevent directory traversal attacks
    config_path = os.path.abspath(config_name)

    # Ensure the file resides within an allowed directory (e.g., /etc/myapp)
    allowed_dir = os.path.abspath("/etc/myapp")
    if not config_path.startswith(allowed_dir):
        raise IOError(f"Access to '{config_name}' is forbidden: outside allowed directory")

    # Read the file content
    try:
        with open(config_path, "r", encoding="utf-8") as fp:
            raw_data = fp.read()
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{config_name}' not found") from exc
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{config_name}': {exc}") from exc

    # Retrieve the trusted signature for this config file
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if not trusted_sig:
        # If no signature is known, refuse to load the file
        return None

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # Parse JSON safely
    try:
        config_dict = json.loads(raw_data)
    except json.JSONDecodeError:
        # Invalid JSON – treat as a signature failure
        return None

    return config_dict