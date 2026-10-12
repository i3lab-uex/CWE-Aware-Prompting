import json
import pathlib
import hmac
from typing import Dict, Optional

# Example trusted signatures mapping. In real use this should be populated
# from a secure source (e.g., environment variable, sealed vault, etc.).
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # 'config.json': 'a1b2c3d4e5f6...',
}

def handle_config_file(file_name: str, sign: str) -> Optional[Dict]:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name of the configuration file to read.
    sign : str
        The cryptographic signature that accompanies the configuration.

    Returns
    -------
    dict | None
        Parsed JSON configuration if the signature matches the trusted one.
        ``None`` if the provided signature is invalid.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path and ensure the file exists
    cfg_path = pathlib.Path(file_name).expanduser().resolve()
    if not cfg_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sig is None:
        raise ValueError(f"No trusted signature registered for '{file_name}'.")

    # Verify the provided signature against the expected one using timing‑safe comparison
    if not hmac.compare_digest(sign.strip(), expected_sig.strip()):
        return None

    # Read and parse the configuration
    try:
        with cfg_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read or parse configuration file '{file_name}': {exc}")

    # Basic type check: ensure the config is a dictionary
    if not isinstance(config, dict):
        raise ValueError(f"Configuration file '{file_name}' does not contain a JSON object.")

    return config