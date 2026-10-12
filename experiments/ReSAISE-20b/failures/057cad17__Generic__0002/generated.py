import json
from pathlib import Path

# Global dictionary mapping trusted signatures to the corresponding config filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; replace with real signatures and filenames.
    "sha256:abcd1234...": "configA.json",
    "sha256:efgh5678...": "configB.json",
}

def handle_config_file(filename: str, sig: str):
    """
    Load a configuration file after validating its cryptographic signature.

    Parameters
    ----------
    filename : str
        Name of the configuration file to load.
    sig : str
        Cryptographic signature that should match the trusted signature for this file.

    Returns
    -------
    dict or None
        The configuration data as a dictionary if the signature is valid;
        otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Verify that the provided signature is trusted for this filename
    expected_filename = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_filename != filename:
        # Signature does not match the requested file
        return None

    # Resolve the path securely to avoid directory traversal attacks
    config_path = Path(filename).resolve()

    # Ensure the file exists; raise IOError if not
    if not config_path.is_file():
        raise IOError(f"Configuration file '{filename}' not found.")

    # Read and parse the configuration (assuming JSON format)
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        # If the file is not valid JSON, treat it as an invalid configuration
        return None