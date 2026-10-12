import json
import csv
from io import BytesIO, TextIOWrapper

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into a Python object using only safe methods.

    Supported formats:
        - 'json' : JSON serialized data
        - 'csv'  : CSV formatted data (returns a list of dicts)

    Parameters
    ----------
    data_bytes : bytes
        The serialized byte stream.
    format_method : str
        Identifier of the serialization method.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_method is not recognized or disallowed.
    """
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be bytes or bytearray")

    method = format_method.lower()
    if method == "json":
        try:
            return json.loads(data_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Interpret the bytes as UTF‑8 encoded CSV data
        try:
            text_stream = TextIOWrapper(BytesIO(data_bytes), encoding="utf-8")
        except Exception as exc:
            raise ValueError("Failed to decode CSV data") from exc

        reader = csv.DictReader(text_stream)
        # Convert the reader to a list of dictionaries
        return [row for row in reader]

    raise ValueError(f"Unsupported or disallowed serialization method: {format_method}")