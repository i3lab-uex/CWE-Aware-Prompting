import json
import hmac
from pathlib import Path

# Example trusted signatures mapping. In real code this should be securely populated.
TRUSTED_CONFIG_SIGNATURES = {
    # signature (hex string) : filename
    "a1b2c3d4e5f6": "config.json",
    # add more trusted signatures here
}

def handle_config_file(filename: str, sig: str) -> dict | None:
    """
    Read a configuration file and return its contents as a dictionary
    only if the provided cryptographic signature is valid.

    Parameters:
        filename (str): Name of the configuration file to read.
        sig (str): Hexadecimal cryptographic signature provided with the data.

    Returns:
        dict | None: Parsed configuration dictionary if signature is valid,
                     otherwise None.

    Raises:
        IOError: If the requested file does not exist or cannot be read.
    """
    # Verify that the signature is trusted for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # No trusted signature for this file
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig.lower(), expected_sig.lower()):
        # Signature does not match
        return None

    config_path = Path(filename)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{filename}' not found.")

    try:
        with config_path.open("r", encoding="utf-8") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{filename}'.") from exc

    try:
        config_data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Configuration file '{filename}' contains invalid JSON.") from exc

    if not isinstance(config_data, dict):
        # The configuration must be a JSON object
        raise ValueError(f"Configuration file '{filename}' does not contain a JSON object.")

    return config_data