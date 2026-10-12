import json

def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized data to deserialize.
    data_format : str
        The format of the serialization. Supported values are:
            - 'json'  (the most secure and widely supported format)

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If `data_format` is unsupported or considered insecure.
    """
    # Only allow safe, explicitly whitelisted formats
    allowed_formats = {"json"}

    fmt_lower = data_format.lower()
    if fmt_lower not in allowed_formats:
        raise ValueError(
            f"Unsupported or insecure deserialization format: '{data_format}'. "
            "Only 'json' is permitted."
        )

    # Perform deserialization
    if fmt_lower == "json":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Data is not valid JSON") from exc