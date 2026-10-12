import json
import hashlib
import os

# Example trusted signatures dictionary (populated elsewhere in the application)
TRUSTED_CONFIG_SIGNATURES = {
    # 'config_file.json': 'expected_sha256_hash_of_the_file',
}


def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name (or relative path) of the configuration file to load.
    cfg_signature : str
        The cryptographic signature (hex digest) expected for the file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve the absolute path of the configuration file
    cfg_path = os.path.abspath(cfg_name)

    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_name}' not found at {cfg_path}")

    # Read the entire content of the file
    try:
        with open(cfg_path, "rb") as f:
            data_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    # Compute the SHA-256 hash of the file content
    computed_hash = hashlib.sha256(data_bytes).hexdigest()

    # Compare the computed hash with the expected signature
    if computed_hash.lower() != cfg_signature.lower():
        # Signature mismatch – do not return the config
        return None

    # Optionally verify against a pre‑known trusted signature list
    expected_trusted = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if expected_trusted and computed_hash.lower() != expected_trusted.lower():
        return None

    # Parse the file content as JSON and return it
    try:
        config = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # If parsing fails we treat it as an invalid configuration
        raise IOError(f"Failed to parse JSON in '{cfg_name}': {exc}") from exc

    return config