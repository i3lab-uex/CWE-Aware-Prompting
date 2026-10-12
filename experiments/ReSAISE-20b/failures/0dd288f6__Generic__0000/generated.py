import json
import hashlib
from pathlib import Path
from typing import Dict, Optional

# Global mapping of configuration filenames to their expected SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values)
    "app_config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd9c4b5e1f4e8e5f3b2",
    "db_config.json":  "c3fcd3d76192e4007dfb496cca67e13b",
}

# Base directory where configuration files are stored.
CONFIG_BASE_DIR = Path("/etc/myapp/configs")


def apply_config_data(configuration_name: str,
                      config_signature: str) -> Optional[Dict]:
    """
    Read a configuration file, validate its cryptographic signature and
    return the parsed JSON data.

    Parameters
    ----------
    configuration_name : str
        The name of the configuration file (e.g., "app_config.json").
    config_signature : str
        The expected cryptographic signature (hex digest) of the file.

    Returns
    -------
    dict or None
        Parsed configuration data if the signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or accessed.
    """
    # Resolve the full path securely, preventing directory traversal
    config_path = (CONFIG_BASE_DIR / configuration_name).resolve()
    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Read the file in binary mode
    try:
        data = config_path.read_bytes()
    except OSError as exc:  # pragma: no cover
        raise IOError(f"Unable to read configuration file '{configuration_name}': {exc}") from exc

    # Compute SHA-256 hash of the file contents
    computed_hash = hashlib.sha256(data).hexdigest()

    # Verify the signature matches both the provided and trusted values
    expected_hash = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if computed_hash != config_signature:
        return None
    if expected_hash is not None and computed_hash != expected_hash:
        return None

    # Parse JSON content
    try:
        config_dict = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise IOError(f"Configuration file '{configuration_name}' contains invalid JSON: {exc}") from exc

    return config_dict