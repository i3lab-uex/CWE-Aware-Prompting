import os
import json
import hmac
from pathlib import Path

# Global mapping of trusted signatures to config file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (signature: filename)
    # "sha256$abcd1234...": "app_config.json",
}
# NOTE: In a real deployment, the signatures would be generated
# using a secure signing algorithm and stored securely.


def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Reads a configuration file and verifies its cryptographic signature.

    Args:
        config_filename: Name of the configuration file to load.
        provided_sig: Signature string supplied alongside the file.

    Returns:
        A dictionary with the configuration data if the signature is valid;
        otherwise, None.

    Raises:
        IOError: If the requested configuration file cannot be found or opened.
    """
    # Prevent path traversal by only allowing a simple filename
    safe_name = os.path.basename(config_filename)
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(safe_name)

    # The signature must exist and match the provided one
    if not expected_sig or not hmac.compare_digest(provided_sig, expected_sig):
        # Signature invalid – do not load the file
        return None

    # Resolve absolute path relative to a predefined config directory
    config_dir = Path(__file__).parent / "configs"
    file_path = config_dir / safe_name

    try:
        with open(file_path, "r", encoding="utf-8") as fp:
            # Assuming JSON configuration; adjust if needed
            data = json.load(fp)
    except FileNotFoundError:
        raise IOError(f"Configuration file '{safe_name}' not found.")
    except json.JSONDecodeError as exc:
        # Malformed config – treat as invalid
        raise IOError(f"Configuration file '{safe_name}' is corrupted: {exc}") from exc

    return data