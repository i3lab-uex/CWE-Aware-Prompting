import json
import os
import hmac

# Global dictionary mapping trusted signatures to their expected filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (hexadecimal signatures for illustration)
    "a1b2c3d4e5f67890123456789abcdef0": "app_config.json",
    "1234567890abcdef1234567890abcdef": "db_settings.yaml",
}

def handle_config_file(filename: str, sig: str):
    """
    Retrieve and validate a configuration file.

    Parameters
    ----------
    filename : str
        Name of the configuration file to read.
    sig : str
        Cryptographic signature accompanying the data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or read.
    """
    # 1. Verify that the provided signature is trusted and matches the requested file.
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if not expected_file or not hmac.compare_digest(expected_file, filename):
        # Signature is either unknown or does not match the requested file.
        return None

    # 2. Ensure the configuration file exists in a secure location.
    config_path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{filename}' not found.")

    # 3. Read and parse the configuration data.
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{filename}': {exc}") from exc

    # 4. Attempt to parse the content as JSON (or other supported format).
    try:
        # Try JSON first; fallback to YAML if json fails and PyYAML is available.
        config_data = json.loads(content)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
            config_data = yaml.safe_load(content)
        except Exception:
            # Unsupported format or parsing error.
            return None

    if not isinstance(config_data, dict):
        # Configuration must be a dictionary.
        return None

    return config_data