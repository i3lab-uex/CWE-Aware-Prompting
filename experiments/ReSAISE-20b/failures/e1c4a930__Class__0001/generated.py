import json
from typing import Any


def deserialize_stream_payload(
    serialized_data: bytes,
    data_format_type: str
) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Only the following formats are considered safe:
        - 'json'

    Parameters
    ----------
    serialized_data : bytes
        The serialized data received from an external source.
    data_format_type : str
        The format of the serialized data ('json', 'pickle', etc.).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Define a whitelist of safe formats
    _SAFE_FORMATS = {
        "json": json.loads,
    }

    # Normalise the format string
    fmt = data_format_type.strip().lower()

    if fmt not in _SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or insecure data format: '{data_format_type}'. "
            "Only 'json' is supported."
        )

    # Decode bytes to string using UTF-8 (most common text encoding)
    try:
        decoded = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "Failed to decode serialized data using UTF-8."
        ) from exc

    # Deserialize safely
    deserializer = _SAFE_FORMATS[fmt]
    try:
        return deserializer(decoded)
    except Exception as exc:  # pragma: no cover
        # Re‑raise as ValueError to keep a consistent API
        raise ValueError(
            f"Deserialization error for format '{data_format_type}'."
        ) from exc