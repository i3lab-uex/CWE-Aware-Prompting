import json
from typing import Any

# Import yaml safely only if available.  If not installed, we simply disallow 'yaml'.
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# Define the set of trusted formats.
_TRUSTED_FORMATS = {
    "json": json.loads,
    # yaml is optional and safe if the library is available.
    **({"yaml": yaml.safe_load} if yaml else {}),
}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize `data_bytes` according to a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format (e.g., 'json', 'yaml').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or trusted.
    """
    # Normalise format string (case‑insensitive).
    fmt = format_string.lower()
    if fmt not in _TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Decode bytes to text.  UTF‑8 is the de‑facto standard for JSON/YAML.
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise ValueError("Data is not valid UTF‑8") from exc

    # Perform the safe deserialization.
    loader = _TRUSTED_FORMATS[fmt]
    try:
        return loader(text)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize data as {format_string!r}") from exc