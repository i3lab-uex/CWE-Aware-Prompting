import json
from typing import Any

# Trusted serialization formats.  Add any additional safe formats here.
TRUSTED_SIGNATURES = {"json", "yaml"}

# Import PyYAML's safe loader if available.  If not, raise an informative error.
try:
    import yaml
except ImportError as exc:  # pragma: no cover
    yaml = None

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize `data` according to the given `signature`.

    Parameters
    ----------
    data : bytes
        The serialized data.
    signature : str
        Format of the serialized data (e.g. 'json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the signature is not in the list of trusted formats.
    RuntimeError
        If a required dependency for a supported format is missing.
    """
    signature = signature.lower()
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format '{signature}'. "
                         f"Supported formats: {sorted(TRUSTED_SIGNATURES)}")

    # Decode bytes to string (UTF-8) for text-based formats
    try:
        text = data.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Data must be UTF-8 encoded text for json/yaml") from exc

    if signature == "json":
        # `json.loads` is safe for untrusted data as it only constructs basic types
        return json.loads(text)

    if signature == "yaml":
        if yaml is None:
            raise RuntimeError("PyYAML is required for YAML deserialization")
        # Use the safe loader to avoid arbitrary code execution
        return yaml.safe_load(text)

    # This point is unreachable due to the earlier check, but kept for completeness
    raise ValueError(f"Unhandled format '{signature}'")