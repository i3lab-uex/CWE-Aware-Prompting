import os
import hashlib

# Example trusted signatures mapping (filename -> expected SHA-256 hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd7b1b2e9f4d5c1f8a0",
    # Add more trusted signatures here
}

def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Verify the integrity of a configuration file using its SHA-256 signature.

    Parameters
    ----------
    cfg_name : str
        The name (or relative path) of the configuration file.
    cfg_signature : str
        The expected cryptographic signature (hex string) for the file.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature matches.
        ``None`` is returned when the signature does not match.

    Raises
    ------
    IOError
        If the configuration file cannot be located or read.
    """
    # Resolve absolute path to guard against relative traversal attacks
    config_path = os.path.abspath(cfg_name)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{cfg_name}' not found")

    # Compute SHA-256 hash of the file contents
    sha256 = hashlib.sha256()
    try:
        with open(config_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    computed_digest = sha256.hexdigest()

    # Compare the computed digest with both the provided signature and
    # the trusted signature list (if present). Use constant-time comparison.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    trusted_digest = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if not _constant_time_compare(computed_digest, cfg_signature):
        # Provided signature does not match the file content
        return None

    if trusted_digest and not _constant_time_compare(computed_digest, trusted_digest):
        # File content does not match the globally trusted signature
        return None

    # Load configuration (assumed JSON for this example)
    import json
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to parse configuration file '{cfg_name}': {exc}") from exc

    return config_data