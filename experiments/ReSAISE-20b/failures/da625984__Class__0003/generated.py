import json
import csv
from io import StringIO, BytesIO
from typing import Any

def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only trusted serialization formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data to be deserialized.
    method_of_serialization : str
        The name of the serialization format. Supported values are:
            - 'json'
            - 'csv'

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the requested serialization method is unsupported or potentially unsafe.
    """
    # Normalize and validate the method name
    fmt = method_of_serialization.strip().lower()
    if fmt not in {"json", "csv"}:
        raise ValueError(f"Unsupported or unsafe serialization format: {method_of_serialization!r}")

    # Decode bytes to text (UTF-8) – a safe assumption for json and csv
    try:
        text = byte_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF-8") from exc

    if fmt == "json":
        # Use json.loads – it never executes arbitrary code
        return json.loads(text)

    if fmt == "csv":
        # Parse CSV into a list of dictionaries
        f = StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # This point should never be reached due to earlier validation
    raise ValueError(f"Unhandled serialization format: {fmt!r}")