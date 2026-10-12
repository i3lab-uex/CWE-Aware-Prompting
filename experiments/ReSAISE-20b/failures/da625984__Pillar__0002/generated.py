import json
import csv
from io import BytesIO, TextIOWrapper, StringIO

# Whitelist of safe serialization formats
TRUSTED_METHODS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str):
    """
    Safely deserialize a byte stream according to the specified serialization method.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    method_of_serialization : str
        The name of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the requested method is not in the trusted whitelist.
    """
    if method_of_serialization.lower() not in TRUSTED_METHODS:
        raise ValueError(f"Unsupported or potentially unsafe serialization method: "
                         f"{method_of_serialization!r}")

    if method_of_serialization.lower() == "json":
        # JSON is safe when used with json.loads
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method_of_serialization.lower() == "csv":
        # CSV can be parsed safely into a list of dictionaries
        try:
            text = byte_data.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return list(reader)
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid CSV data") from exc

    # This point should never be reached because of the whitelist check
    raise ValueError(f"Unhandled serialization method: {method_of_serialization!r}")