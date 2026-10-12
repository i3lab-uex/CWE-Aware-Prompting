import json
import msgpack

# Define the set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "msgpack"}

def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    serialization_format : str
        Format of the serialized data. Must be one of the allowed formats.

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested, or if the data cannot be decoded.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    if fmt == "json":
        try:
            # JSON expects text, so decode using UTF-8 first.
            text = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "msgpack":
        try:
            return msgpack.unpackb(stream, raw=False)
        except Exception as exc:  # msgpack can raise various errors
            raise ValueError("Invalid MessagePack data") from exc

    # This point should never be reached due to the ALLOWED_FORMATS check.
    raise ValueError(f"Unhandled format: {serialization_format}")