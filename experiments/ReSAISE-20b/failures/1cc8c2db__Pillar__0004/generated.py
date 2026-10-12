import json
from typing import Any

# Import yaml only if available; otherwise, raise at import time.
try:
    import yaml
except ImportError as exc:
    raise RuntimeError("PyYAML is required for YAML deserialization") from exc

# Trusted signatures – only these formats are allowed.
TRUSTED_SIGNATURES = {"json", "yaml"}


def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize data from an untrusted source.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    signature : str
        The format of the serialized data (e.g. 'json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided signature is not in TRUSTED_SIGNATURES.
    """
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Decode bytes to text for JSON/YAML
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if signature == "json":
        # json.loads is safe for basic data structures
        return json.loads(text)

    if signature == "yaml":
        # yaml.safe_load prevents arbitrary code execution
        return yaml.safe_load(text)

    # This point is unreachable due to the earlier check,
    # but added for type safety.
    raise ValueError(f"Unhandled signature: {signature}")