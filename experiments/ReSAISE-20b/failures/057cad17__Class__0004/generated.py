import json
import os

# Global mapping of valid signatures to the names of configuration files they sign.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; replace with real signatures in production
    "d41d8cd98f00b204e9800998ecf8427e": "default.cfg",
    # Add more <signature>: <filename> pairs here
}


def handle_config_file(filename: str, sig: str):
    """
    Read a configuration file only if its cryptographic signature is trusted.

    Parameters
    ----------
    filename : str
        The name of the configuration file to read.
    sig : str
        A cryptographic signature claimed to be associated with the file.

    Returns
    -------
    dict or None
        Parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Verify that the signature is known and matches the requested file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(sig)
    if expected_file != filename:
        # Signature does not match the file or is unknown
        return None

    # Ensure the file exists before attempting to read it
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' is missing.")

    try:
        with open(filename, "r", encoding="utf-8") as fh:
            # Assuming the configuration is in JSON format.
            config = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        # Wrap any file or parsing error in an IOError
        raise IOError(f"Failed to read configuration '{filename}': {exc}") from exc

    return config