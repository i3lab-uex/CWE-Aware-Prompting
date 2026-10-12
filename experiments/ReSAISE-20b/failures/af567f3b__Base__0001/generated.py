import json
import msgpack

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object using only
    explicitly supported and safe formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        One of the supported formats: 'json', 'msgpack'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise ValueError("input_data must be bytes or bytearray")

    fmt = input_format.lower()

    if fmt == "json":
        # JSON is text based; decode bytes to string safely
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    elif fmt == "msgpack":
        # MessagePack is binary; use safe unpacking
        try:
            return msgpack.unpackb(input_data, raw=False)
        except Exception as exc:  # msgpack may raise various exceptions
            raise ValueError("Malformed MessagePack data") from exc

    else:
        # Any other format is disallowed
        raise ValueError(f"Unsupported or insecure deserialization format: {input_format}")