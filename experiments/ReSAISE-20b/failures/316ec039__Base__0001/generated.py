import json
import csv
from io import StringIO, BytesIO
from typing import Any

# List of trusted serialization formats
_TRUSTED_METHODS = {"json", "csv"}


def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize ``serialized_data`` using a trusted method.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream containing the serialized data.
    deserialization_method : str
        Name of the serialization format. Supported values are 'json' and 'csv'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the method is unsupported or potentially unsafe.
    """
    method = deserialization_method.lower()
    if method not in _TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")

    # Ensure the data is decoded safely as UTF‑8
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Serialized data is not valid UTF‑8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Use csv.DictReader to return a list of dictionaries
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")