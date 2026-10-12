import json

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Safely deserialize data from a trusted set of formats.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object in byte form.
    method : str
        Serialization format. Currently only 'json' is allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unsupported or potentially dangerous.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise ValueError("Input must be bytes or bytearray")

    # Only allow JSON. Pickle, XML, and other formats are considered unsafe.
    if method.lower() != 'json':
        raise ValueError(f"Unsupported or dangerous format: {method}")

    # Decode bytes to string using UTF-8 (common for JSON).
    try:
        text = encoded_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Encoded data is not valid UTF-8") from exc

    # Use json.loads which only constructs basic Python data types.
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc