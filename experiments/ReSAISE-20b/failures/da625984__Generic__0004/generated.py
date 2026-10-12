import json
import csv
from io import BytesIO, TextIOWrapper

# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into a Python object using only trusted
    serialization formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    method_of_serialization : str
        One of the supported formats: 'json' or 'csv'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not supported or potentially harmful.
    """
    fmt = method_of_serialization.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization method: {fmt}")

    # Decode bytes to text (UTF-8 is the default for JSON and CSV)
    try:
        text_stream = TextIOWrapper(BytesIO(byte_data), encoding="utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode byte data: {exc}") from exc

    if fmt == "json":
        # json.loads can handle a string or file-like object
        try:
            return json.load(text_stream)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "csv":
        # Read CSV into a list of dictionaries
        reader = csv.DictReader(text_stream)
        return [row for row in reader]

    # This point should never be reached because of the earlier check
    raise ValueError(f"Unhandled serialization method: {fmt}")