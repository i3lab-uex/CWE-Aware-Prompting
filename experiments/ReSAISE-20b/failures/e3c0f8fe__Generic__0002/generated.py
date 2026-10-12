import json
from typing import Any

# Registry of trusted serialization methods.
TRUSTED_METHODS = {
    'json': json.loads,
    # Add other safe serializers here if needed, e.g.:
    # 'msgpack': msgpack.unpackb,
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from a byte stream using a trusted serialization method.

    Parameters
    ----------
    serialized_bytes : bytes
        The data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format (e.g. 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unrecognized or not considered safe.
    """
    if serialization_method not in TRUSTED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method!r}")

    # Retrieve the appropriate deserializer.
    deserializer = TRUSTED_METHODS[serialization_method]

    try:
        if serialization_method == 'json':
            # JSON expects a text string, so decode the bytes first.
            return deserializer(serialized_bytes.decode('utf-8'))
        else:
            # For other serializers that accept bytes directly.
            return deserializer(serialized_bytes)
    except Exception as exc:
        # Wrap any underlying errors in a ValueError to keep the API consistent.
        raise ValueError(f"Failed to deserialize using {serialization_method!r}: {exc}") from exc