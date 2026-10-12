import json
from typing import Any


def deserialize_stream_payload(serialized_data: bytes, data_format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream containing the serialized data.
    data_format_type : str
        A string indicating the serialization format. Only ``'json'`` is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or insecure format is requested.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise TypeError("serialized_data must be bytes or bytearray")

    fmt = data_format_type.lower()

    if fmt == "json":
        # JSON is safe for deserialization as long as the input is trusted
        try:
            return json.loads(serialized_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc
    else:
        raise ValueError(f"Unsupported or insecure format: {data_format_type!r}")