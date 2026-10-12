import json
import csv
import io
from typing import Any, Iterable


# Define the set of accepted serialization formats.
ACCEPTED_FORMATS = {"json", "csv"}


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize the given raw byte data according to the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized data stream.
    format_type : str
        The serialization format used ('json', 'csv').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_type is not in ACCEPTED_FORMATS or if deserialization fails.
    """
    fmt = format_type.lower()
    if fmt not in ACCEPTED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type}")

    try:
        if fmt == "json":
            # JSON is safe to load from trusted sources.
            text = raw_data.decode("utf-8")
            return json.loads(text)

        if fmt == "csv":
            # Parse CSV into a list of dictionaries (first row as header).
            text = raw_data.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc