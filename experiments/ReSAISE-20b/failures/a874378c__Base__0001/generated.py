import json

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe and
    explicitly supported formats.

    Parameters:
        byte_stream (bytes): The serialized data.
        data_format (str): Identifier of the format ('json').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or insecure.
    """
    # Normalize format string
    fmt = data_format.strip().lower()

    if fmt == 'json':
        try:
            # Decode bytes to string assuming UTF-8 encoding
            text = byte_stream.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Byte stream is not valid UTF-8") from exc

        try:
            # Use json.loads which safely parses JSON into Python objects
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc
    else:
        # Reject all other formats to avoid insecure deserialization
        raise ValueError(f"Unsupported or insecure data format: {data_format}")