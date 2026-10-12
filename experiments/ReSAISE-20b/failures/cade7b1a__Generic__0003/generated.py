import json
from pathlib import Path

# Global mapping of configuration file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_config.json": "sha256:abcd1234...",
    # Add actual trusted signatures here.
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load (e.g., "app_config.json").
    signature : str
        The cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found.
    """
    # Resolve the path to the configuration file
    config_path = Path(config_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_name}' not found")

    # Verify the signature
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if trusted_sig is None or signature != trusted_sig:
        # Signature does not match the trusted value
        return None

    # Read and parse the configuration file (assumed to be JSON)
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # If the file cannot be parsed or read, treat it as invalid
        return None

    if not isinstance(data, dict):
        # Configuration must be a dictionary
        return None

    return data