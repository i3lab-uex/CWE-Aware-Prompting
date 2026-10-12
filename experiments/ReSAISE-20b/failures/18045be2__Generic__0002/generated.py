import os
import json
import hashlib

# Global mapping of trusted signatures to configuration file names.
# Example: {'<hex_sha256>': 'config.json', ...}
TRUSTED_CONFIG_SIGNATURES = {
    # Populate with actual trusted signatures
}

def _secure_path(base_dir: str, filename: str) -> str:
    """
    Resolve a file path safely within the given base directory.
    Prevents path traversal attacks by normalizing and ensuring
    the final path is still within `base_dir`.
    """
    base_path = os.path.abspath(base_dir)
    target_path = os.path.abspath(os.path.join(base_path, filename))
    if not target_path.startswith(base_path + os.sep):
        raise ValueError("Attempted path traversal in configuration file name.")
    return target_path

def _compute_sha256(file_bytes: bytes) -> str:
    """Return the hexadecimal SHA-256 digest of the given bytes."""
    sha = hashlib.sha256()
    sha.update(file_bytes)
    return sha.hexdigest()

def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Reads the configuration file `config_file`, verifies that its
    SHA‑256 hash matches `provided_signature` and that the signature
    is listed in TRUSTED_CONFIG_SIGNATURES for this file.
    
    Parameters
    ----------
    config_file : str
        Name of the configuration file to load.
    provided_signature : str
        Cryptographic signature supplied alongside the config data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if verification succeeds,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    ValueError
        If a security violation is detected (e.g., path traversal).
    """
    # Resolve the file path safely
    try:
        config_path = _secure_path(".", config_file)
    except ValueError as exc:
        raise IOError(f"Invalid configuration file path: {config_file}") from exc

    # Read the file contents
    try:
        with open(config_path, "rb") as f:
            data_bytes = f.read()
    except FileNotFoundError as exc:
        raise IOError(f"Configuration file not found: {config_file}") from exc
    except OSError as exc:
        raise IOError(f"Error reading configuration file: {config_file}") from exc

    # Compute the hash of the data
    computed_sig = _compute_sha256(data_bytes)

    # Verify that the provided signature matches the computed one
    if computed_sig != provided_signature:
        return None

    # Verify that this signature is trusted for the given file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if expected_file != config_file:
        return None

    # Parse the configuration data (assumed to be JSON)
    try:
        config_dict = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If parsing fails, treat as invalid
        return None

    return config_dict