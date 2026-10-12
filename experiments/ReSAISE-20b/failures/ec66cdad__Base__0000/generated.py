import json
from typing import Any

# Optional: msgpack can be used if installed, but we keep it optional
try:
    import msgpack  # type: ignore
except ImportError:   # pragma: no cover
    msgpack = None


def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    byte_data : bytes
        Serialized data to be deserialized.
    serialization_type : str
        Format of the serialized data. Supported values are:
            - 'json'   : JSON encoded bytes (UTF‑8)
            - 'msgpack': MessagePack encoded bytes

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization_type is not supported or msgpack is unavailable.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    stype = serialization_type.lower()

    if stype == "json":
        # JSON is safe when loaded from a trusted source; ensure UTF‑8 decoding.
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:  # pragma: no cover
            raise ValueError("Invalid UTF-8 encoding for JSON data") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError("Malformed JSON data") from exc

    if stype == "msgpack":
        if msgpack is None:  # pragma: no cover
            raise ValueError("msgpack module not installed")
        try:
            # strict_map_key ensures keys are immutable types
            return msgpack.unpackb(
                byte_data,
                raw=False,  # decode bytes to str
                strict_map_key=True,
            )
        except Exception as exc:  # pragma: no cover
            raise ValueError("Malformed MessagePack data") from exc

    # Unsupported format
    raise ValueError(f"Unsupported serialization type: {serialization_type}")