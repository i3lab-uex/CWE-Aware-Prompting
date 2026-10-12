import os
import json
import hashlib

# Global dictionary containing the correct signatures for trusted config files.
# The keys are file names and the values are the expected SHA‑256 hex digests of
# those files' contents.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd3b1"
                       "c0c5f2e4d8e9b7",
    # Add more trusted file signatures here
}

def _compute_file_hash(file_path: str) -> str:
    """
    Compute the SHA‑256 hash of a file's contents and return it as a hex string.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def handle_config_data(file_name: str, file_signature: str) -> dict | None:
    """
    Retrieve configuration data from *file_name* and verify its cryptographic
    signature before returning it.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to read.
    file_signature : str
        Signature provided with the configuration data.

    Returns
    -------
    dict | None
        Parsed JSON configuration if the signature is valid; otherwise `None`.

    Raises
    ------
    IOError
        If *file_name* does not exist.
    """
    # Ensure the file exists; raise an IOError if it doesn't
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Compute the actual hash of the file's contents
    try:
        actual_hash = _compute_file_hash(file_name)
    except Exception as exc:  # pragma: no cover
        # If we cannot read the file for any reason, treat it as invalid.
        return None

    # Verify that the provided signature matches both:
    #   1) The expected signature for this file (trusted list)
    #   2) The actual hash of the file's contents
    expected_hash = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if not expected_hash:
        # No trusted signature known for this file
        return None

    if (file_signature.lower() != expected_hash.lower() or
            actual_hash.lower() != expected_hash.lower()):
        # Signature mismatch – data may have been tampered with
        return None

    # If we reach this point, the file is authentic. Parse it as JSON.
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        # Malformed JSON or I/O error – treat as invalid
        return None

    if not isinstance(config_data, dict):
        # Expect a dictionary; otherwise it's an unexpected format
        return None

    return config_data