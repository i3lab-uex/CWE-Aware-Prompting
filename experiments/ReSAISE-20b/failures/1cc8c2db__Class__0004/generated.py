import json
from typing import Any

# Optional: use PyYAML if available; otherwise fall back to a safe stub.
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# List of trusted signature formats.
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize the given byte string `data` according to the specified
    `signature`. Only trusted formats are allowed. Unsupported signatures
    raise a ValueError.

    Parameters:
        data (bytes): The serialized data to be deserialized.
        signature (str): Format of the serialization ('json', 'yaml').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the signature is not in TRUSTED_SIGNATURES.
        ImportError: If yaml support is requested but PyYAML is not installed.
    """
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Convert bytes to string assuming UTF-8 encoding.
    text = data.decode("utf-8")

    if signature == "json":
        # json.loads is safe for JSON; it does not execute code.
        return json.loads(text)

    if signature == "yaml":
        if yaml is None:
            raise ImportError("PyYAML is required for YAML deserialization.")
        # yaml.safe_load avoids executing arbitrary tags.
        return yaml.safe_load(text)

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled signature: {signature}")