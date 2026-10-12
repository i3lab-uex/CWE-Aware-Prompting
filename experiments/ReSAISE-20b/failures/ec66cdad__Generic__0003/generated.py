import json
import msgpack  # type: ignore[import]
from typing import Any


def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Safely deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized stream of data.
    serialization_type : str
        The format of the serialized data. Supported formats are:
            - 'json'   : JSON encoded bytes (UTF‑8).
            - 'msgpack': MessagePack encoded bytes.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization_type is not supported or considered unsafe.
    """
    # Normalise format string to lowercase
    fmt = serialization_type.strip().lower()

    if fmt == "json":
        # JSON is safe because it only produces basic data types.
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF‑8 encoded") from exc
        return json.loads(text)

    if fmt == "msgpack":
        # MessagePack can produce arbitrary Python objects, but we
        # restrict it to basic types by using strict=True.
        try:
            return msgpack.unpackb(byte_data, raw=False, strict_map_key=True)
        except Exception as exc:
            raise ValueError("Failed to deserialize MessagePack data") from exc

    # If we reach this point, the format is unsupported
    raise ValueError(f"Unsupported or unsafe serialization type: {serialization_type}")