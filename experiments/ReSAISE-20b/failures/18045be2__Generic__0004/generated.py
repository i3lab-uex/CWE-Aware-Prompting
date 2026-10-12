import json
from pathlib import Path

# Example trusted signatures mapping.
# In practice this should be populated securely, e.g. from a signed manifest.
TRUSTED_CONFIG_SIGNATURES = {
    # "signature": "config_file_name"
    "abc123def456ghi789jkl012mno345pq": "app_config.json",
    # Add more trusted signatures here
}


def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Load a configuration file only if the supplied cryptographic signature is trusted.

    Parameters
    ----------
    config_file : str
        Name of the configuration file to load.
    provided_signature : str
        Cryptographic signature that should match the trusted mapping.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # 1. Verify that the provided signature is trusted for this file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if expected_file != config_file:
        # Signature does not match the file or is unknown
        return None

    # 2. Attempt to read the configuration file safely
    try:
        config_path = Path(config_file).resolve(strict=True)
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file '{config_file}' not found") from exc

    try:
        with config_path.open("r", encoding="utf-8") as fp:
            raw_data = fp.read()
    except OSError as exc:  # Covers permission errors, etc.
        raise IOError(f"Failed to read configuration file '{config_file}'") from exc

    # 3. Parse the data as JSON (adjust if a different format is required)
    try:
        config_data = json.loads(raw_data)
    except json.JSONDecodeError as exc:
        raise IOError(f"Configuration file '{config_file}' contains invalid JSON") from exc

    # 4. Return the parsed configuration
    return config_data


# Example usage (commented out – remove or adapt in real code)
# if __name__ == "__main__":
#     config = verify_config_data("app_config.json", "abc123def456ghi789jkl012mno345pq")
#     if config is None:
#         print("Invalid signature or untrusted configuration.")
#     else:
#         print("Loaded config:", config)