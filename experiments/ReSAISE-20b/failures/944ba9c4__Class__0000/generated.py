import json
from pathlib import Path
from typing import Dict, Optional

# Global dictionary mapping filenames to their trusted cryptographic signatures.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with actual trusted signatures.
    "config1.json": "a3f5c7d9e2b4...",
    "config2.yaml": "1b4f6a8d0c9e..."
}


def validate_config_file(filename: str, cryptographic_signature: str) -> Optional[Dict]:
    """
    Load a configuration file and verify that its cryptographic signature matches the
    trusted signature stored in TRUSTED_CONFIG_SIGNATURES.

    Parameters
    ----------
    filename : str
        Path to the configuration file.
    cryptographic_signature : str
        The signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Resolve the path and ensure the file exists
    config_path = Path(filename)
    if not config_path.is_file():
        raise IOError(f"Configuration file '{filename}' does not exist.")

    # Retrieve the expected signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_signature is None:
        # No trusted signature known for this file; treat as invalid
        return None

    # Perform a constant‑time comparison to mitigate timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    if not _constant_time_compare(cryptographic_signature, expected_signature):
        # Signature mismatch – reject the file
        return None

    # Read and parse the configuration file (support JSON or YAML if needed)
    try:
        with config_path.open("r", encoding="utf-8") as fp:
            if filename.lower().endswith(".json"):
                config_data = json.load(fp)
            else:
                # For non‑JSON formats, simply return the raw text.
                config_data = fp.read()
    except Exception as exc:
        # Any I/O or parsing error results in a failure to validate.
        return None

    if isinstance(config_data, dict):
        return config_data
    # If the file content is not a dictionary (e.g., raw string), reject it.
    return None