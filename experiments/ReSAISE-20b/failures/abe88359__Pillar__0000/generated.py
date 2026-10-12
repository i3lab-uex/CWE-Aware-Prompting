import os
import hashlib
import hmac
import json

# Global dictionary mapping configuration file names to their expected SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: 'app_config.json': '3a7bd3e2360a...',
}

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Verify the integrity of a configuration file by checking its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name of the configuration file to read.
    cfg_signature : str
        The SHA‑256 signature provided by the caller (e.g., from a manifest).

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is verified,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(cfg_name):
        raise IOError(f"Configuration file '{cfg_name}' not found.")

    try:
        with open(cfg_name, "rb") as f:
            content = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{cfg_name}': {exc}") from exc

    # Compute the SHA‑256 digest of the file contents
    computed_digest = hashlib.sha256(content).hexdigest()

    # Retrieve the trusted signature for this file (if any)
    trusted_digest = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)

    # Validate the provided signature against both the computed digest and the trusted digest
    signatures_match = (
        hmac.compare_digest(computed_digest, cfg_signature)
        and (trusted_digest is None or hmac.compare_digest(computed_digest, trusted_digest))
    )

    if not signatures_match:
        return None

    # Parse the configuration (assuming JSON format)
    try:
        config = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # If the file is corrupted or not JSON, treat it as invalid
        return None

    return config