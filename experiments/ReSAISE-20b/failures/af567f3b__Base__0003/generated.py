import json

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data that needs to be deserialized.
    input_format : str
        A string indicating the deserialization format (e.g., 'json').

    Returns
    -------
    object
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    # Define a whitelist of safe formats
    _SAFE_FORMATS = {
        "json": json.loads,
    }

    # Normalize format string
    fmt_key = input_format.strip().lower()

    if fmt_key not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {input_format!r}")

    # Decode bytes to string (UTF-8 is the common encoding for JSON)
    try:
        text = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Input data is not valid UTF-8 encoded text: {exc}") from exc

    # Perform the deserialization
    try:
        return _SAFE_FORMATS[fmt_key](text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON data: {exc}") from exc