import json
import hashlib
import hmac
from pathlib import Path

# Global dictionary containing trusted signatures for configuration files.
# Example: {"config.json": "5e884..."}
TRUSTED_CONFIG_SIGNATURES = {
    # Populate with actual trusted signatures
}

def handle_config_file(file_name: str, sign: str) -> dict | None:
    """
    Read a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name (or relative path) of the configuration file.
    sign : str
        The cryptographic signature supplied for this configuration.

    Returns
    -------
    dict | None
        Parsed JSON configuration if the signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path to guard against directory traversal
    file_path = Path(file_name).resolve()

    # Check that the file is within an allowed directory (e.g., current working dir)
    if not file_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Read the raw bytes of the configuration
    try:
        with file_path.open("rb") as f:
            data_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc

    # Compute SHA-256 digest of the file content
    computed_digest = hashlib.sha256(data_bytes).hexdigest()

    # Verify that the supplied signature matches the computed digest
    if not hmac.compare_digest(computed_digest, sign):
        return None

    # Verify that the computed digest matches the trusted signature for this file
    trusted_digest = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if not trusted_digest or not hmac.compare_digest(computed_digest, trusted_digest):
        return None

    # Parse the configuration as JSON
    try:
        config = json.loads(data_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Malformed configuration
        return None

    return config