import os
import hashlib

# Example trusted signatures dictionary. In a real system this would be populated
# from a secure source or hard‑coded in a protected module.
TRUSTED_CONFIG_SIGNATURES = {
    "config.yaml": "3f1e2c4d5a6b7c8d9e0f123456789abcdeffedcba9876543210fedcba9876543",
    "settings.json": "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789",
    # Add more trusted filenames and their SHA‑256 signatures here
}


def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    file_signature : str
        Signature provided alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature matches trusted value;
        otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Read the raw bytes of the configuration file
    with open(file_name, "rb") as f:
        data_bytes = f.read()

    # Compute SHA‑256 hash of the file content
    computed_hash = hashlib.sha256(data_bytes).hexdigest()

    # Check that the provided signature matches the computed hash
    if computed_hash != file_signature:
        return None

    # Verify that this filename is trusted and the signature matches
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if not trusted_sig or trusted_sig != file_signature:
        return None

    # Parse the configuration data depending on file format
    try:
        if file_name.endswith((".yaml", ".yml")):
            import yaml
            config = yaml.safe_load(data_bytes)
        elif file_name.endswith(".json"):
            import json
            config = json.loads(data_bytes.decode("utf-8"))
        else:
            # Unsupported file format
            return None

        if not isinstance(config, dict):
            # Expecting a dictionary structure for configuration
            return None

        return config
    except Exception:
        # Any parsing error results in a failure to load the configuration
        return None