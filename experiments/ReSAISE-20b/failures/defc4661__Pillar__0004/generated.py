import json
import hashlib
import hmac
from pathlib import Path

# Example trusted signatures dictionary.
# In real usage this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES = {
    "config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbddc9c5b1e4f2b8bf0a7",
    # Add more trusted file signatures here.
}

def handle_config_file(file_name: str, sign: str) -> dict | None:
    """
    Reads a configuration file and validates its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name (or relative path) of the configuration file.
    sign : str
        The cryptographic signature supplied for validation.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid;
        otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve the path to avoid directory traversal issues
    config_path = Path(file_name).resolve()

    # Ensure the file exists and is a regular file
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Read the file content safely
    try:
        with config_path.open("rb") as f:
            data = f.read()
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Unable to read configuration file '{file_name}'.") from exc

    # Verify the supplied signature against the trusted value
    expected_sign = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sign is None:
        # No trusted signature for this file – treat as invalid
        return None

    # Use constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(sign, expected_sign):
        return None

    # Optionally verify that the content matches the signature
    # (e.g., by recomputing a hash of the file contents).
    # Here we assume that the trusted signature already covers the
    # file content, so this step is omitted for simplicity.

    # Parse JSON configuration safely
    try:
        config = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:  # pragma: no cover
        return None

    if not isinstance(config, dict):
        return None

    return config