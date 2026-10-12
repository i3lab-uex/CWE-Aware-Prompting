import json

try:
    import msgpack  # optional, may not be installed
except ImportError:  # pragma: no cover
    msgpack = None


def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object for a limited set of safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        Format identifier. Supported values are:
            - 'json'      : JSON data (UTF‑8 encoded).
            - 'msgpack'   : MessagePack data.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported, insecure, or deserialization fails.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise ValueError("Input data must be bytes or bytearray.")

    fmt = data_format_type.lower()
    if fmt == "json":
        try:
            # JSON is text; decode using UTF‑8
            return json.loads(serialized_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data.") from exc

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("MessagePack support not available (missing dependency).")
        try:
            # Strict map key ensures keys are hashable, preventing malicious objects
            return msgpack.unpackb(
                serialized_data,
                strict_map_key=True,
                raw=False,  # decode strings to str
            )
        except Exception as exc:
            raise ValueError("Failed to deserialize MessagePack data.") from exc

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported or insecure data format: {data_format_type}")