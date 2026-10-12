import json
import csv
from io import TextIOWrapper, BytesIO
from typing import Any

# Whitelist of safe serialization methods
TRUSTED_METHODS = {
    "json": _deserialize_json,
    "csv":  _deserialize_csv,
}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Recover a Python object from a serialized byte stream using only
    trusted serialization methods.

    Parameters:
        deserialized_bytes (bytes): The raw data to be deserialized.
        method_for_serialization (str): Name of the serialization format
            (e.g., 'json', 'csv').

    Returns:
        Any: The Python object obtained from the byte stream.

    Raises:
        ValueError: If the serialization method is unsupported or
            potentially unsafe.
    """
    # Normalise method name to lowercase for case‑insensitive matching
    method = method_for_serialization.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or unsafe serialization method: '{method_for_serialization}'. "
            f"Allowed methods: {', '.join(TRUSTED_METHODS.keys())}"
        )

    # Delegate to the appropriate deserializer
    return TRUSTED_METHODS[method](deserialized_bytes)


def _deserialize_json(data: bytes) -> Any:
    """
    Deserialize JSON data from a byte string.
    """
    try:
        text = data.decode("utf-8")
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize JSON: {exc}") from exc


def _deserialize_csv(data: bytes) -> list[dict[str, str]]:
    """
    Deserialize CSV data from a byte string into a list of dictionaries.
    Each row becomes a dict mapping column names to string values.

    This is safe because the csv module does not evaluate or execute
    code from the input.
    """
    try:
        with BytesIO(data) as bio, TextIOWrapper(bio, encoding="utf-8") as text_stream:
            reader = csv.DictReader(text_stream)
            return list(reader)
    except Exception as exc:
        raise ValueError(f"Failed to deserialize CSV: {exc}") from exc