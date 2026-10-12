import json

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
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `data_format` is not in the list of allowed formats.
    """
    # Normalise format string (case‑insensitive)
    fmt = data_format.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: '{data_format}'. "
                         f"Allowed formats are: {sorted(ALLOWED_FORMATS)}")

    # Convert bytes to a string for JSON deserialization
    if isinstance(data, bytes):
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data could not be decoded as UTF‑8.") from exc
    else:
        raise TypeError("Data must be of type 'bytes'.")

    # Perform the deserialization
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse JSON data.") from exc