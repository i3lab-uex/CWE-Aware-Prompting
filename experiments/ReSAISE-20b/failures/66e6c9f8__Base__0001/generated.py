import json
import msgpack

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "msgpack"}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    stream_format : str
        The format of the serialized data. Only formats listed in SAFE_FORMATS
        are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS.
    """
    fmt = stream_format.lower()
    if fmt == "json":
        # JSON is text based; decode bytes to str before loading.
        try:
            return json.loads(stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

    if fmt == "msgpack":
        # msgpack is binary. Use strict_map_key to avoid unsafe keys.
        try:
            return msgpack.unpackb(
                stream,
                strict_map_key=True,
                raw=False  # Decode bytes keys/values to str
            )
        except (msgpack.ExtraData, msgpack.FormatError, msgpack.StackError) as exc:
            raise ValueError(f"Failed to deserialize msgpack: {exc}") from exc

    # If we reach here, the format is unsupported.
    raise ValueError(f"Unsupported or insecure format: {stream_format}")