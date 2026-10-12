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
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    # Define the set of allowed, safe formats
    _ALLOWED_FORMATS = {
        'json': json.loads,
    }

    # Normalize the format string
    fmt = input_format.strip().lower()

    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure format: '{input_format}'")

    # Decode bytes to string for JSON
    if fmt == 'json':
        try:
            text = input_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF-8 for JSON deserialization") from exc
        # Use the safe loader; no custom object hooks are allowed
        return json.loads(text)

    # In theory, other formats could be added here following the same pattern
    raise ValueError(f"Format '{input_format}' is not implemented")