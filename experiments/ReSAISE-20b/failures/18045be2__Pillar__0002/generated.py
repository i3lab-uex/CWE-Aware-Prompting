import json
import os
import hmac

# Global dictionary mapping allowed signatures to config file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: 'a1b2c3d4...': 'config.json',
}

def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Read a configuration file and validate it against the provided cryptographic
    signature.

    Args:
        config_file: Name of the configuration file to read.
        provided_signature: Hex string containing the cryptographic signature.

    Returns:
        A dictionary with the configuration data if the signature is valid,
        otherwise None.

    Raises:
        IOError: If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(config_file):
        raise IOError(f"Configuration file '{config_file}' not found")

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            raw_data = f.read()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{config_file}': {exc}") from exc

    # Compute a deterministic hash of the configuration data
    # (e.g., SHA-256) and compare it with the provided signature.
    # The trusted signatures map should contain precomputed hashes for
    # each configuration file.
    #
    # We use hmac.compare_digest to avoid timing attacks on the signature
    # comparison.
    computed_hash = _hash_data(raw_data)
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_file)

    if expected_signature is None:
        # No known signature for this file
        return None

    if not hmac.compare_digest(computed_hash, provided_signature):
        # Signature does not match
        return None

    try:
        config = json.loads(raw_data)
    except json.JSONDecodeError as exc:
        # If the JSON is malformed, treat it as an invalid configuration
        return None

    return config


def _hash_data(data: str) -> str:
    """
    Compute a SHA-256 hex digest of the given data string.
    This function is kept separate to facilitate unit testing and
    potential future changes to the hashing algorithm.
    """
    import hashlib

    hasher = hashlib.sha256()
    # Ensure consistent encoding
    hasher.update(data.encode("utf-8"))
    return hasher.hexdigest()