import json

__all__ = ["decode_data_stream"]

# Define the list of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialized data. Only formats listed in
        ``ALLOWED_FORMATS`` are permitted.

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If ``data_format`` is not in ``ALLOWED_FORMATS`` or if the data cannot
        be decoded according to that format.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    if fmt == "json":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # This point should never be reached because of the ALLOWED_FORMATS check,
    # but it's kept for future-proofing if new formats are added.
    raise ValueError(f"Unhandled format: {data_format!r}")