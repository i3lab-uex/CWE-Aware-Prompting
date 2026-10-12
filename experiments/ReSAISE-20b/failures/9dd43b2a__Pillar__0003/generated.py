import json
import html

# List of formats considered safe for deserialization
SAFE_FORMATS = {"json", "html"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object only for trusted formats.

    Parameters
    ----------
    content : bytes
        Serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g., 'json', 'html').

    Returns
    -------
    object
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(content, bytes):
        raise TypeError("content must be a bytes object")

    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Decode bytes to string using UTF-8; ignore errors for robustness
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("content is not valid UTF-8") from exc

    if fmt == "json":
        # json.loads safely parses JSON into Python objects
        return json.loads(text)

    if fmt == "html":
        # For HTML, we simply unescape entities. No structured parsing is done.
        return html.unescape(text)

    # This point should never be reached due to the SAFE_FORMATS check
    raise ValueError(f"Unhandled format: {format_type}")