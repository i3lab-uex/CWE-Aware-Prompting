import os
import json
import hmac

# Global dictionary mapping trusted signatures to the names of configuration files.
# Example:
# TRUSTED_CONFIG_SIGNATURES = {
#     "abc123...": "config1.json",
#     "def456...": "config2.yaml"
# }
TRUSTED_CONFIG_SIGNATURES = {}

def handle_config_file(filename: str, sig: str):
    """
    Retrieve and verify a configuration file using its cryptographic signature.

    Parameters
    ----------
    filename : str
        The name of the configuration file to retrieve.
    sig : str
        The cryptographic signature provided with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    ValueError
        If the configuration file contains invalid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Verify that the supplied signature is trusted for this file.
    # ------------------------------------------------------------------
    # Use constant‑time comparison to mitigate timing attacks (CWE‑347).
    trusted = False
    for expected_sig, expected_file in TRUSTED_CONFIG_SIGNATURES.items():
        if hmac.compare_digest(sig, expected_sig) and filename == expected_file:
            trusted = True
            break

    if not trusted:
        # Signature does not match the expected mapping.
        return None

    # ------------------------------------------------------------------
    # 2. Ensure the file exists and read it.
    # ------------------------------------------------------------------
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' not found.")

    with open(filename, "r", encoding="utf-8") as fh:
        try:
            config = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in configuration file '{filename}'.") from exc

    return config