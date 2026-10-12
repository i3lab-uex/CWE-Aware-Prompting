import json
from pathlib import Path

# Global dictionary mapping trusted signatures to their corresponding filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real signatures in production
    "a1b2c3d4e5f6g7h8i9j0": "config1.json",
    "1234567890abcdef1234": "settings.yaml",
}

def handle_config_file(filename: str, sig: str):
    """
    Read and validate a configuration file using a cryptographic signature.

    Parameters
    ----------
    filename : str
        Name of the configuration file to read.
    sig : str
        Cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or opened.
    """
    # Verify that the signature is trusted and corresponds to the requested file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Signature does not match the file – do not expose any data
        return None

    config_path = Path(filename)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{filename}' not found")

    try:
        with config_path.open("r", encoding="utf-8") as f:
            # Attempt to parse the file as JSON; fallback to YAML if needed
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If JSON parsing fails, try YAML
                import yaml  # Lazy import to avoid unnecessary dependency
                f.seek(0)
                return yaml.safe_load(f)
    except Exception as exc:
        # Re‑raise as IOError to conform to the contract
        raise IOError(f"Failed to read configuration file '{filename}': {exc}") from exc