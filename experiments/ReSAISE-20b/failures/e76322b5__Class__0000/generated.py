import json
import csv
from io import TextIOWrapper, BytesIO

# Allowed serialization formats – only safe ones are permitted
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str):
    """
    Deserialize a byte stream into a Python object using the specified format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        The name of the serialization format ('json' or 'csv').

    Returns
    -------
    object
        The deserialized Python object.  For JSON it is a native Python data
        structure (dict, list, etc.).  For CSV it is a list of dictionaries,
        each representing a row keyed by column headers.

    Raises
    ------
    ValueError
        If the format_name is not in ALLOWED_FORMATS or if deserialization fails.
    """
    # Normalise format name
    fmt = format_name.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_name!r}")

    # JSON deserialization
    if fmt == "json":
        try:
            return json.loads(encoded_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    # CSV deserialization
    if fmt == "csv":
        try:
            # Wrap the bytes in a text IO object for csv module
            with TextIOWrapper(BytesIO(encoded_bytes), encoding="utf-8") as txt:
                reader = csv.DictReader(txt)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"Invalid CSV data: {exc}") from exc