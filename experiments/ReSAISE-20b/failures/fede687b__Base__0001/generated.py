import json
import csv
from io import StringIO
from typing import Any


# A set of serialization formats that are considered safe for untrusted data.
ALLOWED_FORMATS = {"json", "csv"}


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize `raw_data` according to the specified `format_type`.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    format_type : str
        One of 'json' or 'csv'.  Any other value will raise ValueError.

    Returns
    -------
    Any
        The Python object produced by deserialization.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of allowed formats.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or insecure serialization format: {format_type!r}. "
            f"Allowed formats are: {', '.join(sorted(ALLOWED_FORMATS))}"
        )

    # Convert bytes to text for JSON and CSV parsing
    try:
        data_text = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data must be valid UTF-8 encoded text") from exc

    if fmt == "json":
        try:
            return json.loads(data_text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # CSV is interpreted as a list of rows, each row being a list of strings.
        reader = csv.reader(StringIO(data_text))
        return [row for row in reader]

    # This point is unreachable because of the format check above.
    raise ValueError(f"Unhandled format: {format_type!r}")