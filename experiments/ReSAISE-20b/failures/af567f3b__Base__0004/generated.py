import json

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data to deserialize.
    input_format : str
        The format of the serialized data. Supported formats: 'json'.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be a bytes object")

    fmt = input_format.lower()
    if fmt == "json":
        try:
            # Decode bytes to string using UTF-8, ignoring errors could lead to data loss
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # Add more safe formats here if needed, e.g. 'msgpack' with a dedicated library

    raise ValueError(f"Unsupported or insecure format: {input_format}")