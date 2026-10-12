import json
import csv
from io import BytesIO, TextIOWrapper

def load_object(serialized_data: bytes, deserialization_method: str):
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The data to be deserialized.
    deserialization_method : str
        One of the supported serialization formats ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not supported or if deserialization fails.
    """
    method = deserialization_method.lower()

    if method == 'json':
        try:
            return json.loads(serialized_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == 'csv':
        try:
            # csv requires text, so decode the bytes first
            text_stream = TextIOWrapper(BytesIO(serialized_data), encoding='utf-8')
            reader = csv.DictReader(text_stream)
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc

    # If we reach here, the method is unsupported
    raise ValueError(f"Unsupported deserialization method: {deserialization_method!r}")