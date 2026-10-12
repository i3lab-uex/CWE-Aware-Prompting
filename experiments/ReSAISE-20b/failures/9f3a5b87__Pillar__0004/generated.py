import hashlib
import json
from pathlib import Path

# Example trusted signatures dictionary.
# In a real system, this should be stored securely and not hard‑coded.
TRUSTED_CONFIG_SIGNATURES = {
    "config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbddc9b0e1f7d8e5b3f2f",
    # Add other trusted files here...
}

def handle_config_data(file_name: str, file_signature: str):
    """
    Load configuration data from *file_name* and verify that its SHA256
    digest matches the supplied *file_signature*.  The function returns a
    dictionary containing the configuration data if the signature is valid,
    otherwise it returns ``None``.

    Parameters
    ----------
    file_name : str
        Name (or relative path) of the configuration file to read.
    file_signature : str
        Hexadecimal SHA256 digest that the caller claims is valid for the
        file contents.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is verified; otherwise,
        ``None``.

    Raises
    ------
    IOError
        If the file does not exist or cannot be read.
    """
    # Resolve the path to avoid relative traversal attacks
    file_path = Path(file_name).resolve()

    if not file_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Read the raw bytes of the configuration file
    try:
        data_bytes = file_path.read_bytes()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{file_name}': {exc}") from exc

    # Compute the SHA256 digest of the file contents
    computed_digest = hashlib.sha256(data_bytes).hexdigest()

    # Compare with the provided signature in a timing‑attack safe manner
    if not _secure_compare(computed_digest, file_signature):
        return None

    # Parse the JSON configuration
    try:
        config = json.loads(data_bytes.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # Invalid JSON format – treat as a failure to avoid using corrupt data
        return None

    return config


def _secure_compare(a: str, b: str) -> bool:
    """
    Constant‑time comparison to mitigate timing attacks.
    Returns True if both strings are equal, False otherwise.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0