import json
from typing import Any

# Import yaml only if available; otherwise provide a fallback warning.
try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

# Trusted signatures – only safe formats are allowed.
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize the given data into a Python object.

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
        If the provided signature is not in TRUSTED_SIGNATURES or if yaml support
        is unavailable when requested.
    """
    signature = signature.lower()
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    # Convert bytes to string for text-based formats.
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise ValueError("Data must be UTF-8 encoded text for json/yaml") from exc

    if signature == "json":
        return json.loads(text)

    if signature == "yaml":
        if yaml is None:  # pragma: no cover
            raise ValueError("PyYAML is not installed; cannot parse yaml.")
        # Use safe_load to avoid executing arbitrary tags.
        return yaml.safe_load(text)

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled format: {signature}")