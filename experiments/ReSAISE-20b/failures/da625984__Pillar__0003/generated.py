import json
import csv
import io
from typing import Any

# Trusted serialization formats
_TRUSTED_METHODS = {
    "json",
    "csv",
}


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize `byte_data` using the specified `method_of_serialization`.

    Parameters
    ----------
    byte_data : bytes
        Serialized data stream.
    method_of_serialization : str
        Serialization format. Supported values are 'json' and 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not supported or data cannot be decoded.
    """
    if method_of_serialization.lower() not in _TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported serialization method: {method_of_serialization!r}. "
            f"Allowed methods are {_TRUSTED_METHODS}"
        )

    # Ensure the bytes can be decoded to text
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"Data cannot be decoded using UTF-8: {exc}"
        ) from exc

    if method_of_serialization.lower() == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    # CSV handling
    if method_of_serialization.lower() == "csv":
        try:
            csv_file = io.StringIO(text)
            reader = csv.DictReader(csv_file)
            return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"Invalid CSV data: {exc}") from exc