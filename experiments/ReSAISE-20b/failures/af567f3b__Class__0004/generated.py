import json

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object while enforcing
    strict format restrictions to mitigate security risks.

    Parameters:
        input_data (bytes): The serialized data.
        input_format (str): Format identifier, e.g., 'json'.

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or deemed insecure.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise ValueError("input_data must be bytes-like")

    # Normalize the format string to lowercase for case-insensitive matching
    fmt = input_format.lower()

    if fmt == "json":
        # Convert bytes to str using UTF-8 (common for JSON)
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF-8 data for JSON deserialization: {exc}") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON decoding failed: {exc}") from exc

    # If we reach here, the format is not supported
    raise ValueError(f"Unsupported or insecure input format: '{input_format}'")