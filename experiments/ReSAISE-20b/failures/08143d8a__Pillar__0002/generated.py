import os
import json
import hmac

# Global dictionary mapping trusted signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: 'a1b2c3d4...': 'config.yaml',
}

def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Retrieve and validate a configuration file.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to retrieve.
    provided_sig : str
        Cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid; otherwise,
        ``None``.  Raises :class:`IOError` if the file cannot be read.

    Notes
    -----
    * The function compares signatures using :func:`hmac.compare_digest`
      to mitigate timing‑attack vulnerabilities (CWE‑693).
    * Only files listed in :data:`TRUSTED_CONFIG_SIGNATURES` are considered
      valid.  This protects against directory traversal and arbitrary file
      access.
    """
    # Ensure the requested filename is one of the trusted names to avoid
    # path traversal or accidental exposure.
    if config_filename not in TRUSTED_CONFIG_SIGNATURES.values():
        raise IOError(f"Configuration file '{config_filename}' is not recognized.")

    # Verify that the provided signature matches the trusted one.
    expected_sig = None
    for sig, fname in TRUSTED_CONFIG_SIGNATURES.items():
        if fname == config_filename:
            expected_sig = sig
            break

    # If we cannot find a matching signature entry, treat it as invalid.
    if expected_sig is None or not hmac.compare_digest(provided_sig, expected_sig):
        return None

    # At this point the signature is trusted; read and parse the file.
    try:
        with open(config_filename, 'r', encoding='utf-8') as f:
            # Assuming the configuration file is in JSON format.
            config_data = json.load(f)
    except FileNotFoundError:
        raise IOError(f"Configuration file '{config_filename}' not found.")
    except json.JSONDecodeError as exc:
        # The file exists but is not valid JSON; treat this as a failure.
        raise IOError(f"Invalid configuration format in '{config_filename}': {exc}")

    return config_data