import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# Define the set of accepted and safe serialization formats.
ALLOWED_FORMATS = {
    'json',
    'csv',
}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input data.
    format_name : str
        Name of the serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or considered insecure.
    """
    if not isinstance(encoded_bytes, (bytes, bytearray)):
        raise TypeError('encoded_bytes must be bytes-like.')

    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name}")

    # ------------------------------------------------------------------
    # JSON deserialization
    # ------------------------------------------------------------------
    if fmt == 'json':
        try:
            text = encoded_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError('Invalid JSON data') from exc

    # ------------------------------------------------------------------
    # CSV deserialization
    # ------------------------------------------------------------------
    if fmt == 'csv':
        try:
            with BytesIO(encoded_bytes) as buffer, TextIOWrapper(buffer, encoding='utf-8') as text_stream:
                reader = csv.reader(text_stream)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError('Invalid CSV data') from exc

    # The code should never reach here because of the earlier check.
    raise ValueError(f"Unhandled format: {format_name}")