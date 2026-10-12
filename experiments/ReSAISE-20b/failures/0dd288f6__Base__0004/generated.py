import json
import pathlib
import hashlib
import hmac

# Example trusted signatures dictionary (filename -> hex SHA256 signature)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more trusted config files and their expected signatures here
}


def _compute_file_signature(file_path: pathlib.Path) -> str:
    """
    Compute the SHA256 hash of the given file and return it as a hex string.
    """
    sha256 = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def apply_config_data(configuration_name: str, config_signature: str) -> dict | None:
    """
    Load a configuration file after verifying its cryptographic signature.

    Args:
        configuration_name: Name of the configuration file (relative to current working directory).
        config_signature: The expected cryptographic signature for the file.

    Returns:
        A dictionary representing the configuration if the signature is verified.
        None if the provided signature does not match the trusted one.

    Raises:
        IOError: If the configuration file cannot be located.
    """
    # Resolve path and ensure file exists
    config_path = pathlib.Path(configuration_name).resolve()
    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Verify the signature against the trusted signatures dictionary
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_signature is None:
        # No trusted signature known for this file
        return None

    # Compute the actual signature of the file content
    actual_signature = _compute_file_signature(config_path)

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(actual_signature, expected_signature):
        return None

    # If the provided config_signature does not match the expected one, reject it
    if not hmac.compare_digest(config_signature, expected_signature):
        return None

    # Load the configuration (assumed to be JSON)
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Any parsing error is treated as a failure to load configuration
        raise IOError(f"Failed to parse configuration file '{configuration_name}': {e}") from e