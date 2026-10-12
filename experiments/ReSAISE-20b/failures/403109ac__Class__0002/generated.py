import json
import csv
import io
from typing import Any, List, Dict

# Define a whitelist of safe serialization formats.
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized data to be deserialized.
    method_type : str
        The serialization format used. Supported values are 'json' and 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method_type is not in ALLOWED_METHODS.
    """
    if method_type not in ALLOWED_METHODS:
        raise ValueError(
            f"Unsupported or insecure serialization method: {method_type!r}"
        )

    if method_type == "json":
        # Decode bytes to string using UTF-8 and parse JSON.
        try:
            text = stream_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if method_type == "csv":
        # Interpret bytes as a CSV document and return a list of dicts.
        try:
            text_stream = io.TextIOWrapper(
                io.BytesIO(stream_bytes), encoding="utf-8", newline=""
            )
            reader = csv.DictReader(text_stream)
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data") from exc