import json
import csv
from io import BytesIO, TextIOWrapper

# List of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data.
    format_method : str
        The serialization method used ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is disallowed or not recognized.
    """
    if format_method.lower() not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed.")

    if format_method.lower() == "json":
        # JSON expects a string, so decode with utf-8
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization.") from exc
        return json.loads(text)

    if format_method.lower() == "csv":
        # CSV is read as text, so wrap the bytes in a TextIOWrapper
        with BytesIO(data_bytes) as bio:
            text_stream = TextIOWrapper(bio, encoding="utf-8")
            reader = csv.DictReader(text_stream)
            return [row for row in reader]

    # Should never reach here because of the earlier check
    raise ValueError(f"Unhandled serialization method: {format_method}")