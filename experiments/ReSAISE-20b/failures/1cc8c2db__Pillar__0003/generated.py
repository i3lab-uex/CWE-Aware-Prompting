import json
from typing import Any

# Import yaml only if available; otherwise raise ImportError at runtime.
try:
    import yaml
except ImportError as exc:
    yaml = None  # yaml support will be unavailable

# List of trusted serialization formats
TRUSTED_SIGNATURES = {"json", "yaml"}


def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize `data` according to the provided `signature`.

    Parameters
    ----------
    data : bytes
        Serialized data from an untrusted source.
    signature : str
        The format of the serialized data ('json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the `signature` is not in the list of trusted signatures.
    ImportError
        If YAML support is requested but PyYAML is not installed.
    """
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature!r}")

    if signature == "json":
        # JSON is safe for deserialization; decode to string first
        text = data.decode("utf-8")
        return json.loads(text)

    if signature == "yaml":
        if yaml is None:
            raise ImportError("PyYAML is required for YAML deserialization")
        text = data.decode("utf-8")
        return yaml.safe_load(text)

    # This point should never be reached due to the check above.
    raise ValueError(f"Unhandled format: {signature!r}")