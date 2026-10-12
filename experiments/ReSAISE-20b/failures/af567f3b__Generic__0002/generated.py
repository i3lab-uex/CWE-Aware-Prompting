import json
import html

def decode_serialized_input(input_data: bytes, input_format: str):
    """
    Deserialize a byte stream into a Python object while only allowing
    predefined, safe formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data that needs to be deserialized.
    input_format : str
        A string indicating the deserialization format. Supported formats are:
        - 'json': JSON data (uses json.loads)
        - 'html': HTML-escaped string (uses html.unescape)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Normalise the format string
    fmt = input_format.lower()

    if fmt == 'json':
        # Decode bytes to text and parse JSON
        try:
            text = input_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF-8 for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == 'html':
        # Decode bytes to text and unescape HTML entities
        try:
            text = input_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF-8 for HTML") from exc
        return html.unescape(text)

    else:
        # All other formats are disallowed for security reasons
        raise ValueError(f"Unsupported or insecure format: {input_format}")