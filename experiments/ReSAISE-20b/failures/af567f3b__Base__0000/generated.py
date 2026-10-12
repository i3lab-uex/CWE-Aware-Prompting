import json

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        Format identifier. Supported values are:
            - 'json'  (default)

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `input_format` is unsupported or insecure.
    """
    # Define the set of safe, supported formats
    SAFE_FORMATS = {"json"}

    fmt = input_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {input_format}")

    if fmt == "json":
        # Decode bytes to text safely
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF-8") from exc

        # Use json.loads which does not allow arbitrary code execution
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc