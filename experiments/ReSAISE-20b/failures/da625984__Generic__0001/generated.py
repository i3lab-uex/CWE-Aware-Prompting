import json
import csv
import io

def deserialize_obj(byte_data: bytes, method_of_serialization: str):
    """
    Safely restore a Python object from serialized byte data.

    Parameters
    ----------
    byte_data : bytes
        The raw byte stream containing the serialized data.
    method_of_serialization : str
        The serialization format. Supported values are:
            - 'json'
            - 'csv'

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    # Normalize and validate the requested format
    fmt = method_of_serialization.lower()
    if fmt not in {"json", "csv"}:
        raise ValueError(f"Unsupported or unsafe serialization method: {method_of_serialization!r}")

    # Decode the byte stream into a string for text-based formats
    try:
        decoded = byte_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF-8") from exc

    if fmt == "json":
        # json.loads is safe for primitive data structures (dict, list, str, int, float, bool, None)
        return json.loads(decoded)

    if fmt == "csv":
        # Use csv.DictReader to parse CSV data into a list of dictionaries
        f = io.StringIO(decoded)
        reader = csv.DictReader(f)
        return list(reader)

    # The code path should never reach here due to the earlier check
    raise ValueError(f"Unhandled serialization format: {fmt!r}")