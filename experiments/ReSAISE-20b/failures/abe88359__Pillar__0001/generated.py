import os
import json
import hashlib

# Global dictionary mapping configuration filenames to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real values in production
    "app_config.json": "3a7bd3e2360a5f4c2b8d1e9c3b6fa7e2c1d5f4a0e8b9c1d3f6a7b8c9d0e1f2g3",
    # Add more trusted config signatures here
}


def verify_configuration_file(cfg_name: str, cfg_signature: str) -> dict | None:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    cfg_name : str
        The filename of the configuration file to read.
    cfg_signature : str
        The cryptographic signature (hex digest) that should match the file's content.

    Returns
    -------
    dict | None
        The parsed configuration as a dictionary if the signature matches.
        Returns None if the provided signature does not match the file's hash.

    Raises
    ------
    IOError
        If the configuration file cannot be found or accessed.
    """
    # Resolve the absolute path to avoid relative path tricks
    cfg_path = os.path.abspath(cfg_name)

    if not os.path.isfile(cfg_path):
        raise IOError(f"Configuration file '{cfg_name}' not found.")

    # Compute the SHA‑256 hash of the file contents
    hasher = hashlib.sha256()
    try:
        with open(cfg_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{cfg_name}': {exc}") from exc

    computed_signature = hasher.hexdigest()

    # Verify that the provided signature matches the computed one
    if computed_signature.lower() != cfg_signature.lower():
        # Signature mismatch – do not trust the file
        return None

    # Optionally verify that the filename is known and trusted
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(cfg_name)
    if not trusted_sig or trusted_sig.lower() != computed_signature.lower():
        # The file is not in the list of trusted signatures
        return None

    # Safely parse JSON content
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # Corrupt or unreadable JSON – treat as invalid
        return None

    if not isinstance(config, dict):
        # Expect configuration to be a mapping
        return None

    return config