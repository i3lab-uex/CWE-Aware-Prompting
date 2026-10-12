import json
from typing import Any

# Define a set of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json": json.loads,
    # Add more safe formats here if desired, e.g. msgpack: lambda b: msgpack.unpackb(b)
}

def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only trusted formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data. Only formats listed in SAFE_FORMATS are allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS or if deserialization fails.
    """
    # Normalize format string to lower case for consistency
    fmt = data_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure data format: '{data_format}'")

    deserializer = SAFE_FORMATS[fmt]

    try:
        if fmt == "json":
            # json.loads expects a str, not bytes; decode using UTF-8
            return deserializer(byte_stream.decode("utf-8"))
        else:
            # For other safe formats that accept bytes directly
            return deserializer(byte_stream)
    except Exception as exc:
        # Wrap any exception from the underlying deserializer in a ValueError
        raise ValueError(f"Deserialization failed for format '{data_format}': {exc}") from exc