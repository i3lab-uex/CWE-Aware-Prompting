import json

# Define the list of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object for trusted formats only.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        Defines the format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type!r}")

    # Only JSON is supported in this safe list.
    if format_type == "json":
        try:
            # Decode bytes to a string using UTF-8 (common for JSON).
            text = content.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Failed to decode JSON content: {exc}") from exc

        try:
            return json.loads(text)
        except Exception as exc:
            raise ValueError(f"Failed to parse JSON content: {exc}") from exc

    # This point should never be reached due to the SAFE_FORMATS check.
    raise ValueError(f"Unhandled format: {format_type!r}")