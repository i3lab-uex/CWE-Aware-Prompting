import hashlib
import hmac
import json
from pathlib import Path

# Example trusted signatures mapping (filename -> expected SHA256 hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    # "config.json": "e3b0c44298fc1c149afbf4c8996fb924..."
}

def _compute_sha256(file_path: Path) -> str:
    """Compute SHA‑256 hex digest of the given file."""
    hasher = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def handle_config_file(file_name: str, sign: str):
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file to load.
    sign : str
        Expected SHA‑256 hex digest for the file content.

    Returns
    -------
    dict | None
        Parsed JSON configuration if signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    config_path = Path(file_name)

    # Ensure the file exists
    if not config_path.is_file():
        raise IOError(f"Configuration file '{file_name}' not found.")

    # Verify the provided signature matches the expected trusted one
    expected_sign = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_sign is None:
        # No trusted signature for this file – reject outright
        return None

    if not hmac.compare_digest(sign.lower(), expected_sign.lower()):
        # Signature does not match the trusted value
        return None

    # Re‑compute the digest of the actual file content to double‑check
    computed_sign = _compute_sha256(config_path)
    if not hmac.compare_digest(computed_sign, sign.lower()):
        # The provided signature does not match the file content
        return None

    # Load and return the configuration as a dictionary
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{file_name}': {exc}") from exc