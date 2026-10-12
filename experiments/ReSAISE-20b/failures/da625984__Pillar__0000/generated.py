import json
import csv
from io import BytesIO, TextIOWrapper, StringIO

# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str):
    """
    Restore a Python object from serialized byte data.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    method_of_serialization : str
        The serialization format ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially harmful.
    """
    fmt = method_of_serialization.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {fmt}")

    # Decode bytes to text using UTF‑8 (common for JSON and CSV)
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF‑8") from exc

    if fmt == "json":
        # json.loads is safe for standard JSON data
        return json.loads(text)

    if fmt == "csv":
        # Return a list of dictionaries, one per row
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # This point should never be reached because of the earlier check
    raise ValueError(f"Unhandled serialization format: {fmt}")