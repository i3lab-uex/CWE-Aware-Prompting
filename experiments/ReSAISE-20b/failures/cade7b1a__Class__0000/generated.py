import json
import os
from pathlib import Path

# Global mapping of trusted configuration names to their expected signatures.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json":   "d41d8cd98f00b204e9800998ecf8427e",
    "db_config.json":    "0cc175b9c0f1b6a831c399e269772661",
    # Add more trusted config signatures here.
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a JSON configuration file and verify its authenticity.

    Parameters
    ----------
    config_name : str
        Name of the configuration file to load (relative to the current working directory).
    signature : str
        Cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.  Raises ``IOError`` if the file cannot be found.

    Notes
    -----
    * This function performs a simple signature comparison against the global
      ``TRUSTED_CONFIG_SIGNATURES`` mapping.  In a real-world scenario you would
      use a proper cryptographic verification method (e.g. HMAC or RSA
      signatures) to avoid CWE-345 vulnerabilities.
    * The function intentionally avoids any form of tampering detection beyond
      the signature check.  If the file contents change without a matching
      signature, it will be rejected.
    """
    # Resolve the file path in a platform‑independent way.
    config_path = Path(config_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Verify the supplied signature against the trusted value.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if expected_sig is None:
        # Unknown configuration: treat as untrusted.
        return None

    if signature.lower() != expected_sig.lower():
        # Signature mismatch – do not load the configuration.
        return None

    # Load and parse the JSON content safely.
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # Any I/O or parsing error results in a failure to provide config data.
        raise IOError(f"Failed to read configuration '{config_name}': {exc}") from exc

    # Ensure the data is a dictionary.
    if not isinstance(data, dict):
        return None

    return data