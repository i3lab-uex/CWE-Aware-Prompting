import json

# Define the set of safe formats that are allowed for deserialization.
ALLOWED_FORMATS = {"json"}

def unpack_serialized_object(byte_data: bytes, struct_format: str):
    """
    Deserialize binary data from an untrusted source using only predefined safe formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data in binary form.
    struct_format : str
        The format used for deserialization (e.g., 'json').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the provided format is not recognized or considered unsafe.
    """
    if struct_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: {struct_format!r}")

    # Currently, only JSON is supported.
    if struct_format.lower() == "json":
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte data is not valid UTF-8 for JSON deserialization") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc