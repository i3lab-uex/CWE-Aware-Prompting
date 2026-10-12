import json
import msgpack

# A whitelist of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {
    "json",
    "msgpack",  # MessagePack: a binary format that doesn't execute code.
}


def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The format of the serialized data. Supported values are:
        - 'json'
        - 'msgpack'

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided serialization_type is not in the allowed list.
    """
    if serialization_type not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe deserialization format: {serialization_type!r}. "
            f"Allowed formats are: {', '.join(sorted(ALLOWED_FORMATS))}"
        )

    if serialization_type == "json":
        # json.loads expects a str, so decode the bytes using UTF-8.
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc
        return json.loads(text)

    if serialization_type == "msgpack":
        # msgpack.unpackb can handle bytes directly. `raw=False` ensures
        # byte strings are decoded to Unicode.
        return msgpack.unpackb(byte_data, raw=False)

    # This point should never be reached due to the whitelist check above.
    raise ValueError(f"Unhandled serialization type: {serialization_type!r}")