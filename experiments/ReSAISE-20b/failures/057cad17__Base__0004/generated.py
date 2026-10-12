import json
import os
import hmac

# Global dictionary mapping trusted signatures to the filenames they are valid for.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (hex digest : filename)
    "a1b2c3d4e5f6g7h8i9j0": "app_config.json",
    # Add real signatures here
}

def handle_config_file(filename: str, sig: str):
    """
    Reads a configuration file only if the provided cryptographic signature
    is trusted for that file.

    Parameters
    ----------
    filename : str
        The name of the configuration file to read.
    sig : str
        The cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or opened.
    """
    # Verify that the signature is trusted for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if not expected_sig:
        # No signature registered for this file
        return None

    # Use constant‑time comparison to avoid timing attacks (CWE‑347)
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # At this point the signature is trusted; read the file
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' not found.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{filename}': {exc}") from exc

    # Parse JSON content into a dictionary
    try:
        config = json.loads(content)
    except json.JSONDecodeError as exc:
        # Invalid JSON; treat as a failed verification
        return None

    if not isinstance(config, dict):
        # Configuration must be a dictionary
        return None

    return config