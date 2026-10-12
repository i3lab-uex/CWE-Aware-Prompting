import json
import os

# Global mapping of config file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries
    "app_config.json": "5f2d1e8c3a7b4e9f...",
    "db_config.json":  "1a2b3c4d5e6f7g8h...",
}

def process_config_data(config_name: str, signature: str):
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
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found.
    """
    # Verify that we have a trusted signature for this config
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if expected_sig is None:
        # No trusted signature registered for this config
        return None

    if expected_sig != signature:
        # Signature does not match the trusted one
        return None

    # Resolve the file path (assume configs are in a "configs" directory)
    config_path = os.path.join("configs", config_name)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            # Use json.load for safe parsing of configuration files
            config_data = json.load(f)
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{config_name}' not found.") from exc
    except json.JSONDecodeError:
        # If the file exists but is not valid JSON, treat it as a failure
        return None

    # Basic type check to ensure the config is a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data