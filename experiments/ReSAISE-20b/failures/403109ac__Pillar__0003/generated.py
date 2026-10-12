import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# Allowed serialization methods.  Pickle is deliberately omitted due to security risks.
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object based on the specified method_type.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object.  For JSON, a dict/list/primitive; for CSV,
        a list of dictionaries (one per row).

    Raises
    ------
    ValueError
        If method_type is not in ALLOWED_METHODS or if the data cannot be parsed.
    """
    # Normalise method_type to lower case and validate
    fmt = method_type.strip().lower()
    if fmt not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type}")

    # Wrap the byte stream in a context‑managed buffer
    with BytesIO(stream_bytes) as buf:
        if fmt == "json":
            # JSON decoding is safe for the allowed data types
            try:
                return json.loads(buf.read().decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise ValueError("Invalid JSON data") from exc

        if fmt == "csv":
            # CSV requires text decoding; use a TextIOWrapper for proper line handling
            try:
                with TextIOWrapper(buf, encoding="utf-8") as text_buf:
                    reader = csv.DictReader(text_buf)
                    # Convert each row to a dict; return as list
                    return [row for row in reader]
            except Exception as exc:
                raise ValueError("Invalid CSV data") from exc

    # The code should never reach here because all cases are handled
    raise ValueError("Unhandled serialization method")