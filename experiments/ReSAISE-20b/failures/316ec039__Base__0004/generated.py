import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any


def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize `serialized_data` using a trusted serialization format.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream to deserialize.
    deserialization_method : str
        One of the supported serialization formats ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `deserialization_method` is not supported or considered unsafe.
    """
    method = deserialization_method.lower()

    if method == "json":
        # JSON is safe because it only contains basic data types
        try:
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method == "csv":
        # CSV is safe as it only yields strings, numbers and lists of dicts
        try:
            # Wrap the bytes stream in a text wrapper for csv.reader
            with TextIOWrapper(BytesIO(serialized_data), encoding="utf-8") as text_stream:
                reader = csv.DictReader(text_stream)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"Invalid CSV data: {exc}") from exc

    # Any other method is considered unsafe
    raise ValueError(
        f"Unsupported or potentially dangerous deserialization method: '{deserialization_method}'"
    )