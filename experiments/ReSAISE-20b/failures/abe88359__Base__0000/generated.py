import hashlib
import hmac
from pathlib import Path
from typing import Dict, Optional

# Global dictionary of trusted signatures: {filename: hex_digest}
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with actual values
    "app.conf": "d2c7e8f9b3a4... (64 hex chars)",
    "db.cfg":   "a1f5c2e4b7d8... (64 hex chars)",
}

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> Optional[Dict]:
    """
    Reads a configuration file and verifies its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name of the configuration file to read.
    cfg_signature : str
        The hexadecimal representation of the expected SHA-256 signature.

    Returns
    -------
    dict or None
        The parsed configuration as a dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve path (relative to current working directory)
    cfg_path = Path(cfg_name).resolve()
    if not cfg_path.is_file():
        raise IOError(f"Configuration file '{cfg_name}' not found")

    # Read raw bytes for signature calculation
    try:
        data = cfg_path.read_bytes()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    # Compute SHA-256 digest
    computed_digest = hashlib.sha256(data).hexdigest()

    # Verify against the trusted signature list
    expected_trusted = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if not expected_trusted:
        # No trusted signature available for this file
        return None

    # Securely compare the provided signature, the computed digest,
    # and the trusted signature
    if not (
        hmac.compare_digest(cfg_signature.lower(), computed_digest) and
        hmac.compare_digest(computed_digest, expected_trusted.lower())
    ):
        return None

    # Parse the configuration file (simple key=value pairs)
    config: Dict[str, str] = {}
    for line in data.decode("utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    return config