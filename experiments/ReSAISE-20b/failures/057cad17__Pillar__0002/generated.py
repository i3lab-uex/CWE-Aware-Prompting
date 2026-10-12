import os
import json
from typing import Dict, Optional

# Global dictionary mapping valid signatures to their corresponding config filenames.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "a1b2c3d4e5f6g7h8i9j0": "app_config.json",
    "1234567890abcdef1234": "db_settings.yaml",
}

# Base directory where configuration files are stored.
CONFIG_BASE_DIR = os.path.join(os.path.dirname(__file__), "configs")


def handle_config_file(filename: str, sig: str) -> Optional[Dict]:
    """
    Retrieve and validate a configuration file.

    Parameters
    ----------
    filename : str
        The name of the configuration file to retrieve.
    sig : str
        The cryptographic signature provided with the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure that the signature is actually trusted for this filename
    expected_filename = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_filename != filename:
        # Signature does not match the requested file
        return None

    # Construct a safe path and prevent directory traversal attacks.
    safe_path = os.path.normpath(os.path.join(CONFIG_BASE_DIR, filename))
    if not safe_path.startswith(CONFIG_BASE_DIR):
        # Attempt to escape the config directory.
        return None

    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            # Attempt to parse JSON; fallback to YAML if needed.
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Simple YAML loader using safe_load if PyYAML is available.
                try:
                    import yaml
                    data = yaml.safe_load(f)
                except Exception:
                    # If YAML parsing fails, treat it as a plain text config.
                    data = f.read()
    except FileNotFoundError:
        raise IOError(f"Configuration file '{filename}' not found.")
    except OSError as exc:
        # Propagate other I/O errors
        raise IOError(f"Error reading configuration file '{filename}': {exc}") from exc

    return data