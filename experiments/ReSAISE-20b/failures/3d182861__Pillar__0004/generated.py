import json

def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data. Supported values are:
            - 'json'  : JSON format

    Returns
    -------
    object
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If `data_format` is unsupported or considered insecure.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError("Input data must be bytes or bytearray.")

    fmt = data_format.lower()
    if fmt == 'json':
        try:
            # Decode bytes to string using UTF-8 (JSON spec requires Unicode)
            text = data.decode('utf-8')
        except Exception as exc:
            raise ValueError("Failed to decode JSON data: " + str(exc)) from exc

        try:
            return json.loads(text)
        except Exception as exc:
            raise ValueError("Failed to parse JSON data: " + str(exc)) from exc

    # If other formats are needed in the future, add them here
    # with explicit safe handling.

    raise ValueError(f"Unsupported or insecure data format: {data_format}")