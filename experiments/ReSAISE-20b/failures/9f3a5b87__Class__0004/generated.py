import os
import hashlib
import hmac

# Example trusted signatures (filename -> hex signature)
TRUSTED_CONFIG_SIGNATURES = {
    "config.yaml": "5f2c3e8b1a4d6f9b0c7e8d5f2a3b4c1d6e7f9a0b1c2d3e4f5a6b7c8d9e0f1234",
    # add more trusted entries here
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA‑256 hash of a file's contents and return it as a hex string.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def handle_config_data(file_name: str, file_signature: str) -> dict | None:
    """
    Retrieve configuration data from `file_name` and verify its signature.

    Parameters
    ----------
    file_name : str
        The name of the configuration file.
    file_signature : str
        The cryptographic signature provided with the data (hex string).

    Returns
    -------
    dict | None
        The configuration dictionary if the signature matches; otherwise, None.

    Raises
    ------
    IOError
        If `file_name` does not exist.
    """
    # Ensure the file exists; raise IOError if it doesn't
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist")

    # Compute the expected signature from the file contents
    try:
        computed_sig = _compute_file_signature(file_name)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Error reading configuration file '{file_name}': {exc}") from exc

    # Compare the computed signature with the supplied one using constant‑time compare
    if not hmac.compare_digest(computed_sig, file_signature):
        # Signature mismatch: treat as untrusted data
        return None

    # Optionally verify against the global trusted signatures list
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if trusted_sig and not hmac.compare_digest(computed_sig, trusted_sig):
        # The file's signature does not match the known trusted value
        return None

    # Load the configuration data (assuming JSON format for safety)
    try:
        import json
        with open(file_name, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception:  # pragma: no cover
        return None

    return config_data