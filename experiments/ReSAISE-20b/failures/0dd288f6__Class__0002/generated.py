import json
import hashlib
from pathlib import Path

# Global mapping of trusted configuration filenames to their expected SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_config.json": "3a7bd3e2360a2c... (hex string)",
    # "db_config.json":   "1f8ac10d2a5b... (hex string)",
}

def _compute_sha256(file_path: Path) -> str:
    """Compute the SHA‑256 hash of a file's contents in hex."""
    sha = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def apply_config_data(configuration_name: str, config_signature: str) -> dict | None:
    """
    Load a configuration file and verify its integrity using the supplied
    cryptographic signature.

    Parameters:
        configuration_name (str): The name of the configuration file.
        config_signature (str): The expected cryptographic signature
            (hex string) for the configuration file.

    Returns:
        dict: The parsed JSON configuration if the signature is verified.
        None: If the provided signature does not match the trusted value
              or the computed hash.

    Raises:
        IOError: If the configuration file cannot be found.
        ValueError: If the JSON is malformed or not a dictionary.
    """
    # Resolve the file path relative to the current working directory
    config_path = Path(configuration_name).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Verify the supplied signature against the trusted mapping
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)
    if expected_sig is None:
        # No trusted signature for this file – treat as untrusted
        return None

    if config_signature.lower() != expected_sig.lower():
        # The caller supplied an incorrect signature – do not trust the file
        return None

    # Compute the actual hash of the file and compare to the supplied signature
    try:
        actual_sig = _compute_sha256(config_path)
    except Exception as exc:  # pragma: no cover
        # Unexpected read error – treat as untrusted
        return None

    if actual_sig.lower() != config_signature.lower():
        # The file content does not match the signature – reject it
        return None

    # At this point the file is verified; load its JSON contents
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Configuration file '{configuration_name}' contains invalid JSON.") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Configuration file '{configuration_name}' does not contain a JSON object.")

    return data