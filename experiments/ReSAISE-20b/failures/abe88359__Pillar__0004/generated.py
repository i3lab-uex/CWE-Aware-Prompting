import hashlib
from pathlib import Path
import hmac

# Global dictionary mapping configuration filenames to their trusted SHA-256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; populate with real values in production
    "app_config.yaml": "3a7bd3e2360a8c5b1f2d6e9c4e8b1d3a0f7e9c5d2b6a4f8e0c1d3b5a7e9f2c4",
    # Add more configurations as needed
}


def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Verify the integrity of a configuration file using its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The name of the configuration file to validate.
    cfg_signature : str
        The expected SHA-256 hexadecimal digest for the configuration file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is verified;
        otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve the file path relative to the current working directory
    cfg_path = Path(cfg_name).resolve()

    if not cfg_path.is_file():
        raise IOError(f"Configuration file '{cfg_name}' not found.")

    # Read the file contents in binary mode
    try:
        with cfg_path.open("rb") as fp:
            data = fp.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    # Compute SHA-256 digest of the file
    computed_digest = hashlib.sha256(data).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_digest, cfg_signature.lower()):
        # Signature mismatch: do not return the configuration
        return None

    # Optionally verify against a trusted signature dictionary
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if trusted_sig and not hmac.compare_digest(computed_digest, trusted_sig.lower()):
        # The provided signature does not match the globally trusted one
        return None

    # Parse configuration (simple YAML example; replace with actual parser if needed)
    try:
        import yaml  # Lazy import to avoid mandatory dependency
        config = yaml.safe_load(data.decode("utf-8"))
    except Exception as exc:
        # If parsing fails, treat it as a verification failure
        raise IOError(f"Failed to parse configuration file '{cfg_name}': {exc}") from exc

    return config