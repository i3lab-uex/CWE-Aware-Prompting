import json
import csv
from io import BytesIO, TextIOWrapper

# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str):
    """
    Safely deserializes `byte_data` according to the specified serialization method.

    Parameters
    ----------
    byte_data : bytes
        The serialized data to be deserialized.
    method_of_serialization : str
        The serialization format, e.g. 'json' or 'csv'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    TypeError
        If `byte_data` is not of type bytes.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    method = method_of_serialization.lower()
    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {method}")

    if method == "json":
        # JSON decoding is safe for basic data types
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if method == "csv":
        # Parse CSV into a list of dictionaries (first row as header)
        try:
            with BytesIO(byte_data) as buffer:
                text_stream = TextIOWrapper(buffer, encoding="utf-8", newline="")
                reader = csv.DictReader(text_stream)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to deserialize CSV data") from exc