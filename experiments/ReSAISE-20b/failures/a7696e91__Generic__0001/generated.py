import json
import configparser
from typing import Any, Dict

# Maximum allowed size for input data (10 MiB)
_MAX_INPUT_SIZE = 10 * 1024 * 1024


def _ensure_safe_size(data: bytes) -> None:
    """Raise an error if the data size exceeds a safe limit."""
    if len(data) > _MAX_INPUT_SIZE:
        raise ValueError(f"Input data exceeds the maximum allowed size of {_MAX_INPUT_SIZE} bytes.")


def _decode_bytes(data: bytes) -> str:
    """Decode the binary input to UTF‑8 string, raising a clear error on failure."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8.") from exc


def _parse_json(data: str) -> Any:
    """Parse JSON data, allowing only safe primitive types."""
    # json.loads already protects against code execution
    return json.loads(data)


def _parse_ini(data: str) -> Dict[str, Dict[str, str]]:
    """Parse INI data and return a nested dictionary."""
    parser = configparser.ConfigParser()
    # configparser expects a file-like object; read_string is safe for in‑memory strings
    parser.read_string(data)
    # Convert to a plain dictionary
    return {
        section: dict(parser.items(section))
        for section in parser.sections()
    }


# Mapping of supported formats to their handler functions
_SUPPORTED_FORMATS = {
    "json": _parse_json,
    "ini": _parse_ini,
}


def load_serialized_content(serialized_input: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data from a trusted source.

    Parameters
    ----------
    serialized_input : bytes
        The raw binary data to deserialize.
    serialization_format : str
        One of the supported formats: 'json' or 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported, data size is too large,
        or decoding/parsing fails.
    """
    if serialization_format not in _SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{serialization_format}'. "
            "Allowed formats are: " + ", ".join(_SUPPORTED_FORMATS.keys())
        )

    _ensure_safe_size(serialized_input)
    decoded = _decode_bytes(serialized_input)

    parser_func = _SUPPORTED_FORMATS[serialization_format]
    return parser_func(decoded)