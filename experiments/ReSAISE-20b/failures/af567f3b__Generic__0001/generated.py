import json
import html

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object while only supporting
    safe, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data that needs to be deserialized.
    input_format : str
        A string indicating the deserialization format (e.g., 'json', 'html').

    Returns
    -------
    object
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes-like")

    fmt = input_format.lower()
    # Decode the byte stream into a text string
    try:
        text = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Unable to decode input data as UTF-8") from exc

    if fmt == "json":
        # JSON is safe for deserialization; it only produces basic data types
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "html":
        # For HTML, we simply unescape entities; no further parsing is done.
        return html.unescape(text)

    else:
        # Any other format is disallowed for security reasons
        raise ValueError(f"Unsupported or insecure deserialization format: {input_format}")