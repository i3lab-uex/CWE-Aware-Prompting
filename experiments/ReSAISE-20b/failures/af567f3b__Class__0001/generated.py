import json

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object using only
    safe, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        Format identifier, e.g., 'json'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise ValueError("input_data must be bytes or bytearray")

    fmt = input_format.lower()

    if fmt == "json":
        try:
            # json.loads accepts str, so decode using UTF-8
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON") from exc
    else:
        # Extendable: add more safe formats here if needed.
        raise ValueError(f"Unsupported or insecure format: {input_format}")