import json
from typing import Any

# Import PyYAML safely; it may not be available in all environments
try:
    import yaml  # type: ignore[import]
except ImportError:
    yaml = None

# List of signatures we trust for deserialization
TRUSTED_SIGNATURES = ["json", "yaml"]


def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize data from an untrusted source only if the format is trusted.

    Parameters
    ----------
    data : bytes
        Serialized data to be deserialized.
    signature : str
        The format of the serialized data (e.g. 'json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in TRUSTED_SIGNATURES or if required libraries are missing.
    """
    # Ensure the signature is lower‑cased for consistency
    sig = signature.lower()

    if sig not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    if sig == "json":
        # json.loads expects a string; decode from bytes
        return json.loads(data.decode("utf-8"))

    if sig == "yaml":
        if yaml is None:
            raise ValueError("PyYAML library is required for YAML deserialization")
        # Use safe_load to avoid arbitrary code execution
        return yaml.safe_load(data.decode("utf-8"))

    # In practice, this line is unreachable because of the earlier check
    raise ValueError(f"Unhandled format: {signature}")