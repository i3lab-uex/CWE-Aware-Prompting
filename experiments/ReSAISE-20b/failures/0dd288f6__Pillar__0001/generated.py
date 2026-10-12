import os
import json
import hashlib
import hmac

# Global dictionary mapping configuration filenames to their expected SHA256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_config.json": "a3b5c6d7e8f9...",
    # Add real trusted signatures here.
}

def _compute_sha256(data: bytes) -> str:
    """
    Compute the SHA256 hash of the given data and return it as a hex string.
    """
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

def apply_config_data(configuration_name: str, config_signature: str):
    """
    Load a configuration file and verify its integrity using the provided
    cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The filename (relative to the current working directory) of the
        configuration file.
    config_signature : str
        The cryptographic signature that should match the trusted signature.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path to guard against directory traversal attacks
    config_path = os.path.abspath(configuration_name)

    # Ensure the file is within an allowed directory (e.g., current working dir)
    if not config_path.startswith(os.getcwd()):
        raise IOError(f"Access to {configuration_name} is forbidden.")

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    try:
        with open(config_path, "rb") as f:
            data = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{configuration_name}': {exc}") from exc

    # Compute the SHA256 hash of the file contents
    computed_signature = _compute_sha256(data)

    # Use constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(computed_signature, config_signature):
        # Signature mismatch; do not expose details
        return None

    # Optionally, verify against the trusted signatures dictionary as an extra check
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_sig is not None:
        if not hmac.compare_digest(computed_signature, expected_sig):
            return None

    # Parse JSON configuration
    try:
        config = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        # Corrupt or invalid JSON; treat as signature failure
        return None

    return config