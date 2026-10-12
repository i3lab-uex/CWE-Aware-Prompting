import json
import csv
import io
from typing import Any

# Allowed serialization formats.  Pickle is intentionally omitted for security reasons.
ALLOWED_FORMATS = {
    "json",
    "csv",   # CSV will be parsed into a list of dictionaries
}


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize raw byte data according to the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        One of the supported serialization formats ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or insecure format is requested.
    """
    # Normalise the format name and validate
    fmt = format_type.strip().lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported serialization format '{format_type}'. "
            "Only JSON and CSV are permitted."
        )

    # Decode the byte stream once; all supported formats expect text.
    try:
        decoded = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "Input data is not valid UTF-8 text; cannot deserialize."
        ) from exc

    # Handle each supported format
    if fmt == "json":
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if fmt == "csv":
        # Use StringIO to avoid creating an actual file on disk
        with io.StringIO(decoded) as csv_file:
            reader = csv.DictReader(csv_file)
            # Read all rows into a list of dictionaries
            return [row for row in reader]

    # This point should never be reached due to the earlier validation
    raise ValueError(f"Unhandled format: {format_type}")