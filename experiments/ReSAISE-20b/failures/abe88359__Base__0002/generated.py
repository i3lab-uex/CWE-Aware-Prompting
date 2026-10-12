import json
from pathlib import Path
import hmac

# Global dictionary mapping configuration filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more trusted signatures here.
}

def verify_configuration_file(cfg_name: str, cfg_signature: str):
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name of the configuration file to load.
    cfg_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature matches the trusted value.
        ``None`` if the supplied signature does not match.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Resolve the path relative to the current working directory
    config_path = Path(cfg_name)

    if not config_path.is_file():
        raise IOError(f"Configuration file '{cfg_name}' not found")

    # Load the configuration data
    try:
        with config_path.open("r", encoding="utf-8") as f:
            cfg_data = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if expected_sig is None:
        # No trusted signature known; treat as invalid
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    if not hmac.compare_digest(cfg_signature, expected_sig):
        return None

    return cfg_data