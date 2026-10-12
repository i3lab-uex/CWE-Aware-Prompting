import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize raw binary data into a Python object based on the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized data stream.
    format_type : str
        Serialization format used ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is unsupported or considered insecure.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: '{format_type}'")

    # JSON deserialization
    if fmt == "json":
        try:
            text = raw_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    # CSV deserialization – return a list of dictionaries (header → value)
    if fmt == "csv":
        try:
            # Wrap bytes in a TextIOWrapper for csv.reader
            with BytesIO(raw_data) as bio:
                text_wrapper = TextIOWrapper(bio, encoding="utf-8", newline="")
                reader = csv.DictReader(text_wrapper)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc

    # The function should never reach this point due to the earlier check,
    # but we keep a defensive fallback.
    raise ValueError(f"Unhandled format: '{format_type}'")