import json

# Define a set of safe, supported formats for deserialization.
_SAFE_FORMATS = {"json"}

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object using only secure, pre-approved formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        The format type of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object corresponding to the provided format.

    Raises
    ------
    ValueError
        If `data_format_type` is not one of the supported, safe formats.
    """
    if data_format_type.lower() not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format_type!r}")

    if data_format_type.lower() == "json":
        try:
            # Decode bytes to string before parsing JSON.
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 encoding for JSON data") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    # In practice this branch is unreachable due to the safe format check above,
    # but it keeps the function exhaustive.
    raise ValueError(f"Unhandled format: {data_format_type!r}")