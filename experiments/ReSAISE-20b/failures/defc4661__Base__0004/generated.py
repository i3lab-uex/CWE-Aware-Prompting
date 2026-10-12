import json
import hashlib
import hmac
from pathlib import Path
from typing import Dict, Optional

# Example trusted signatures dictionary (file_name -> hex SHA‑256 signature)
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # 'config.json': 'a1b2c3d4e5f6...',
}

def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Reads a configuration file and verifies its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name of the configuration file to read.
    sign : str
        The cryptographic signature (hex digest) that should match the file's contents.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches; otherwise `None`.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve path to avoid directory traversal attacks
    config_path = Path(file_name).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found")

    # Read the raw bytes of the configuration file
    try:
        with config_path.open("rb") as f:
            data_bytes = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{file_name}': {exc}") from exc

    # Compute the SHA‑256 digest of the file contents
    computed_digest = hashlib.sha256(data_bytes).hexdigest()

    # Ensure the provided signature matches the expected one
    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    expected_sign = TRUSTED_CONFIG_SIGNATURES.get(file_name)

    if not expected_sign or not hmac.compare_digest(computed_digest, expected_sign):
        # Signature mismatch – do not trust the configuration
        return None

    # If the provided signature matches, also compare it to the user‑supplied sign
    if not hmac.compare_digest(computed_digest, sign):
        return None

    # Parse the configuration as JSON
    try:
        config = json.loads(data_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        # If the file is not valid JSON, treat it as invalid
        return None

    if not isinstance(config, dict):
        # The configuration must be a dictionary
        return None

    return config