import os
import hashlib

# Example trusted signatures dictionary. In real usage this would be populated from a secure source.
TRUSTED_CONFIG_SIGNATURES = {
    # 'config.yaml': 'a3f1e2b4c5d6...',
}

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Reads a configuration file and verifies its authenticity using the supplied signature.

    Parameters
    ----------
    cfg_name : str
        Path to the configuration file relative to the current working directory.
    cfg_signature : str
        The expected cryptographic signature (hex string) of the file.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature matches; otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path to avoid directory traversal attacks
    abs_path = os.path.abspath(cfg_name)

    # Ensure the file resides within an allowed directory (e.g., current working dir)
    if not abs_path.startswith(os.getcwd()):
        raise IOError(f"Access to '{cfg_name}' is denied: outside of allowed directory.")

    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{cfg_name}' not found.")

    # Read the entire file in binary mode
    try:
        with open(abs_path, "rb") as f:
            data = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{cfg_name}': {exc}") from exc

    # Compute SHA-256 hash of the file contents
    computed_hash = hashlib.sha256(data).hexdigest()

    # Compare with both the supplied signature and the trusted dictionary entry
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if computed_hash != cfg_signature and (expected_sig is None or computed_hash != expected_sig):
        # Signature mismatch; do not expose the raw data
        return None

    # Attempt to parse configuration as JSON or YAML if needed.
    # For demonstration, we simply return a dict with the raw data length.
    # Replace this with actual parsing logic as required.
    return {"file": cfg_name, "size_bytes": len(data)}