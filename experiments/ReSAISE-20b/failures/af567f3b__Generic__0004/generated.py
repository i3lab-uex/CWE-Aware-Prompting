import json
from typing import Any

# yaml is optional – only used if available and explicitly allowed.
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize ``input_data`` from the given format into a Python object.

    Parameters
    ----------
    input_data : bytes
        The serialized data that needs to be deserialized.
    input_format : str
        One of the supported, safe formats. Currently 'json' and (if yaml is available)
        'yaml'.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If ``input_format`` is unsupported or the required library for that format
        (e.g., PyYAML) is not available.
    """
    # Normalise format name
    fmt = input_format.lower()

    try:
        text = input_data.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Input data must be valid UTF-8 encoded bytes") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except Exception as exc:  # pragma: no cover
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        if yaml is None:  # pragma: no cover
            raise ValueError("PyYAML not installed – cannot parse YAML")
        try:
            return yaml.safe_load(text)
        except Exception as exc:  # pragma: no cover
            raise ValueError("Invalid YAML data") from exc

    # Unsupported format
    raise ValueError(f"Unsupported or insecure deserialization format: {input_format}")