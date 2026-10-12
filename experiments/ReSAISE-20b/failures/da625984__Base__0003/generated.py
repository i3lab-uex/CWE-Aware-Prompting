import json
import csv
from io import StringIO
from typing import Any

# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize a Python object from serialized byte data.

    Parameters
    ----------
    byte_data : bytes
        The raw byte stream containing the serialized data.
    method_of_serialization : str
        The serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous serialization method is requested.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    method = method_of_serialization.lower()
    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported serialization method: {method_of_serialization}")

    # Decode bytes to text using UTF-8; errors='strict' ensures decoding failure raises an exception
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF-8 encoded text") from exc

    if method == "json":
        # json.loads is safe for untrusted data as it only constructs basic Python types
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # CSV is treated as a list of dictionaries (each row)
        try:
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")