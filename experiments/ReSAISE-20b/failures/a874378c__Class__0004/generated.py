import json
from typing import Any


def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data. Supported values are:
            - 'json'   : JSON (text-based) format.
            - 'str'    : Raw string representation of a Python literal
                         (e.g., "42", "[1, 2, 3]", '{"a": 1}').  
                         The string is parsed with ``ast.literal_eval`` for safety.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If ``data_format`` is not one of the supported formats or if the data cannot be parsed.
    """
    import ast

    # Normalise format string
    fmt = data_format.strip().lower()

    if fmt == "json":
        try:
            # JSON is text-based; decode using UTF-8
            return json.loads(byte_stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "str":
        try:
            # Decode to string, then use literal_eval for safe evaluation
            text = byte_stream.decode("utf-8")
            return ast.literal_eval(text)
        except (UnicodeDecodeError, ValueError, SyntaxError) as exc:
            raise ValueError("Invalid string literal") from exc

    # Unsupported or insecure format
    raise ValueError(f"Unsupported data format: {data_format!r}")