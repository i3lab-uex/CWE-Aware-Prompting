import json
import os
import hmac

# Example trusted signatures mapping (signature -> config filename)
TRUSTED_CONFIG_SIGNATURES = {
    # 'sha256-hmac-of-config1': 'config1.json',
    # 'sha256-hmac-of-config2': 'config2.yaml',
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Reads a configuration file and validates its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        The name of the configuration file to load.
    provided_sig : str
        The cryptographic signature supplied alongside the config data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Verify that the signature is trusted for this filename
    expected_filename = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if expected_filename is None or not hmac.compare_digest(expected_filename, config_filename):
        # Signature does not match the requested file
        return None

    # Attempt to read the configuration file
    try:
        with open(config_filename, "r", encoding="utf-8") as fp:
            content = fp.read()
    except OSError as exc:
        raise IOError(f"Configuration file '{config_filename}' not available") from exc

    # Parse the configuration data (JSON format assumed)
    try:
        config = json.loads(content)
    except json.JSONDecodeError as exc:
        # If parsing fails, treat it as an invalid configuration
        return None

    return config