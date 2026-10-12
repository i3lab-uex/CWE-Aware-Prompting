import json

# Define a set of safe, supported formats.
ALLOWED_FORMATS = {
    "json": _decode_json,
}

def _decode_json(data: bytes):
    """
    Decode JSON data from a byte stream.

    Parameters
    ----------
    data : bytes
        The serialized JSON data.

    Returns
    -------
    Any
        The Python object represented by the JSON data.
    """
    # Convert bytes to string using UTF-8.  Errors are handled by raising a
    # UnicodeDecodeError, which is appropriate for malformed input.
    text = data.decode("utf-8")
    return json.loads(text)


def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object for a safe format.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or considered unsafe.
    """
    if data_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe data format: {data_format!r}. "
            "Allowed formats are: "
            f"{', '.join(sorted(ALLOWED_FORMATS))}."
        )

    # Retrieve the appropriate decoder function and invoke it.
    decode_func = ALLOWED_FORMATS[data_format.lower()]
    return decode_func(data)