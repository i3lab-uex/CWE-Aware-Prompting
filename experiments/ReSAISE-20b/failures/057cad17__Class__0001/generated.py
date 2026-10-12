import os
import json
import hmac

# Global dictionary mapping trusted signatures to allowed filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "sha256:abcd1234...": "config.yaml",
}

def handle_config_file(filename: str, sig: str):
    """
    Read a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    filename : str
        The name of the configuration file to read.
    sig : str
        The cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be opened.
    """
    # 1. Verify that the signature is trusted for this filename
    expected_filename = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if not expected_filename or not hmac.compare_digest(expected_filename, filename):
        # Signature is invalid or does not match the requested file
        return None

    # 2. Ensure the file exists and is readable
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' not found.")

    # 3. Read and parse the configuration file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # Assuming JSON format; adjust if a different format is used
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Propagate file I/O errors and JSON parsing issues
        raise IOError(f"Failed to read or parse configuration file '{filename}': {exc}") from exc

    return config