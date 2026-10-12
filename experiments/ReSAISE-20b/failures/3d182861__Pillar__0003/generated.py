import json
import html


def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialization. Supported values are:
            - 'json'   : JSON encoded data.
            - 'html'   : HTML-escaped string (decoded to a plain string).

    Returns
    -------
    object
        The Python representation of the data.

    Raises
    ------
    ValueError
        If `data_format` is not supported or considered insecure.
    """
    if data_format.lower() == "json":
        try:
            # JSON requires a text string, so decode bytes first
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if data_format.lower() == "html":
        try:
            # Decode bytes to a string and unescape HTML entities
            return html.unescape(data.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to deserialize HTML data") from exc

    # If the format is not explicitly supported, reject it
    raise ValueError(f"Unsupported or insecure data format: {data_format}")