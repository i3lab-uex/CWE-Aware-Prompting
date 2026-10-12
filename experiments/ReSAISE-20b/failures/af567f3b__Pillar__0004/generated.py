import json

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object in a safe manner.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        The format of the serialization. Only 'json' is supported.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If `input_format` is not supported or considered insecure.
    TypeError
        If `input_data` is not of type `bytes`.
    """
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be of type 'bytes'")

    # Only allow a small, safe set of formats
    if input_format.lower() != "json":
        raise ValueError(f"Unsupported or insecure format: {input_format!r}")

    # Decode bytes to string safely
    try:
        text = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8 encoded JSON") from exc

    # Parse the JSON safely
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Input data is not valid JSON") from exc