import json
import hmac
from pathlib import Path
from typing import Dict, Optional

# Global mapping of valid signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with actual signatures.
    "app_config.json": "d2b3c1f0e8a9...",
    "db_settings.yaml": "4f7a2b1c3d5e..."
}


def verify_config_data(config_file: str, provided_signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify that its signature matches the trusted value.

    Parameters
    ----------
    config_file : str
        The name of the configuration file to read.
    provided_signature : str
        The cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Resolve the path and ensure the file exists
    config_path = Path(config_file)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_file}' not found")

    # Retrieve the trusted signature for this configuration
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_file)
    if expected_signature is None:
        # If we have no record of this file, treat it as untrusted
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE-693)
    if not hmac.compare_digest(provided_signature, expected_signature):
        return None

    # Read and parse the configuration data
    try:
        with config_path.open("r", encoding="utf-8") as f:
            # Support JSON; extend to other formats if needed
            config_data = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers file I/O errors; ValueError for JSON parsing errors
        raise IOError(f"Failed to read or parse '{config_file}': {exc}") from exc

    return config_data