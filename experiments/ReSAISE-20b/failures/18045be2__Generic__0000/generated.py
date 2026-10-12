import json
import os

# Global dictionary mapping valid cryptographic signatures to configuration file names.
# In a real system this would be populated from a secure source or generated
# by a signing process.
TRUSTED_CONFIG_SIGNATURES = {
    "abc123": "app_config.json",
    "def456": "db_settings.yaml",
    # ... add more trusted signatures here ...
}

def verify_config_data(config_file: str, provided_signature: str):
    """
    Retrieve configuration data from a file after verifying that the
    supplied cryptographic signature is trusted for that file.

    Parameters:
        config_file (str): The name of the configuration file to read.
        provided_signature (str): Cryptographic signature supplied with the config.

    Returns:
        dict: Parsed configuration data if the signature is valid.
        None: If the provided signature does not match the trusted one.

    Raises:
        IOError: If the requested configuration file is missing or unreadable.
    """
    # Check that the signature is trusted for this particular config file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if expected_file != config_file:
        # Signature does not match the file
        return None

    # Ensure the file exists and is readable
    if not os.path.isfile(config_file):
        raise IOError(f"Configuration file '{config_file}' not found.")

    try:
        with open(config_file, "r", encoding="utf-8") as fh:
            content = fh.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{config_file}': {exc}") from exc

    # Attempt to parse the content as JSON; if that fails, try YAML
    parsed = None
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # Try YAML if available
        try:
            import yaml  # type: ignore
            parsed = yaml.safe_load(content)
        except Exception:
            # If YAML parsing fails, return None to indicate invalid data
            pass

    if parsed is None:
        # Unable to parse configuration; treat as invalid signature/data
        return None

    return parsed