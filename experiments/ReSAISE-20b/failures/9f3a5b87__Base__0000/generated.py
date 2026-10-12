import json
from pathlib import Path
import hmac

# Global dictionary mapping file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_config.json": "a1b2c3d4e5f6...",
    # Add actual file-signature pairs here.
}

def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Args:
        file_name (str): Name of the configuration file.
        file_signature (str): Cryptographic signature sent with the data.

    Returns:
        dict | None: Parsed configuration dictionary if signature is valid; otherwise, None.

    Raises:
        IOError: If the requested file does not exist.
    """
    config_path = Path(file_name)

    # Ensure the file exists
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Read the file content (assuming JSON format)
    try:
        raw_data = config_path.read_text(encoding="utf-8")
    except Exception as exc:
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc

    # Verify the signature in a timing‑safe manner
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if trusted_sig is None:
        # No known signature for this file – treat as untrusted
        return None

    if not hmac.compare_digest(file_signature, trusted_sig):
        # Signature mismatch
        return None

    # Parse JSON into a dictionary
    try:
        config_dict = json.loads(raw_data)
    except json.JSONDecodeError as exc:
        # Malformed JSON – treat as invalid
        return None

    return config_dict