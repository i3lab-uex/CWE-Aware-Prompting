import json

# A small, explicit whitelist of safe formats for deserialization.
# Only the formats listed here are allowed; everything else will raise a ValueError.
_ALLOWED_FORMATS = {
    'json': lambda b: json.loads(b.decode('utf-8')),
}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialized data. Must be one of the keys in
        `_ALLOWED_FORMATS`.

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `data_format` is not in the whitelist of allowed formats.
    """
    if data_format.lower() not in _ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe data format: '{data_format}'. "
            "Only the following formats are allowed: "
            f"{', '.join(_ALLOWED_FORMATS.keys())}"
        )

    # Retrieve the deserialization function for the requested format
    deserialize_fn = _ALLOWED_FORMATS[data_format.lower()]

    try:
        return deserialize_fn(data)
    except Exception as exc:  # pragma: no cover
        # Wrap any deserialization error in a ValueError to avoid leaking
        # low-level exception details that could aid an attacker.
        raise ValueError(f"Failed to deserialize data as {data_format}") from exc