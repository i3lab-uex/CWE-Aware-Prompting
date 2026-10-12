import json
import csv
import io
from typing import Any, Iterable


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize ``raw_data`` according to ``format_type``.

    Supported formats (case‑insensitive):
        - 'json' : returns a Python object obtained from json.loads
        - 'csv'  : returns a list of dictionaries (one per row) using csv.DictReader

    Any other format raises ``ValueError`` to avoid insecure or unsupported
    deserialization methods.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        The serialization format identifier.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If ``format_type`` is not in the list of allowed formats.
    """
    if not isinstance(raw_data, (bytes, bytearray)):
        raise TypeError("raw_data must be bytes or bytearray")

    fmt = format_type.lower()

    if fmt == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        try:
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("CSV data must be UTF‑8 encoded") from exc

        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    raise ValueError(f"Unsupported or insecure format: {format_type!r}")