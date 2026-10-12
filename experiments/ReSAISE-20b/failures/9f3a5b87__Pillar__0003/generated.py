import os
import json
import hashlib
import hmac

# Example trusted signatures dictionary.
# Keys are filenames, values are the expected hex‑encoded SHA256 digests.
TRUSTED_CONFIG_SIGNATURES = {
    # "config.json": "3a7bd3e2360a... (full SHA256 digest)",
}

def _compute_file_digest(file_path: str) -> str:
    """
    Compute the SHA256 digest of a file's contents in a memory‑efficient way.
    Returns the hex digest string.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from *file_name*, verify that the provided
    *file_signature* matches the trusted signature for this file, and return
    the configuration as a dictionary.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    file_signature : str
        Hex‑encoded cryptographic signature (e.g., SHA256 digest) supplied with the file.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If *file_name* does not exist or cannot be opened.
    """
    # Verify the file exists
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Compute the digest of the file
    computed_digest = _compute_file_digest(file_name)

    # Fetch the trusted digest for this file
    trusted_digest = TRUSTED_CONFIG_SIGNATURES.get(file_name)

    # If no trusted signature is defined for this file, consider it invalid
    if not trusted_digest:
        return None

    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(computed_digest, trusted_digest):
        return None

    # Verify that the supplied signature matches the computed digest
    if not hmac.compare_digest(computed_digest, file_signature):
        return None

    # Load the configuration as JSON
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        # Any error while parsing the JSON is treated as invalid
        return None

    if not isinstance(config, dict):
        # Configuration must be a dictionary
        return None

    return config