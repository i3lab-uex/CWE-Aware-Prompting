import json
import msgpack

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object for safe and supported formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        Format of the serialized data. Supported values are:
            - 'json'
            - 'msgpack'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the data format is unsupported or considered insecure.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise TypeError("serialized_data must be bytes or bytearray")

    fmt = data_format_type.lower()

    if fmt == "json":
        try:
            # JSON expects a string, so decode using UTF-8
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "msgpack":
        try:
            # msgpack.unpackb defaults to returning bytes for string keys; set raw=False
            return msgpack.unpackb(serialized_data, strict_map_key=True, raw=False)
        except Exception as exc:
            raise ValueError("Invalid msgpack data") from exc

    # If we reach here, the format is unsupported
    raise ValueError(f"Unsupported or insecure data format: {data_format_type!r}")