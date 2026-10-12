import json

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data that needs to be deserialized.
    input_format : str
        A string indicating the deserialization format. Supported formats are:
            - 'json'

    Returns
    -------
    Any
        The corresponding Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    # Normalise format string to lowercase for case‑insensitive comparison
    fmt = input_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF‑8, then parse JSON
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON data: {exc}") from exc
    else:
        # Only 'json' is allowed; all other formats are rejected to avoid security risks
        raise ValueError(f"Unsupported or insecure deserialization format: '{input_format}'")