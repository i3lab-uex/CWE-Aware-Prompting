import json
import csv
from io import StringIO
from typing import Any, List, Dict


# List of serialization formats that are considered safe for deserialization
TRUSTED_FORMATS = {"json", "csv"}


def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Restore a Python object from serialized data.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized object.
    deserialization_method : str
        The serialization format used ('json', 'csv', etc.).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    # Normalise method name to lower case
    method = deserialization_method.strip().lower()

    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")

    # Decode bytes to string using UTF-8; this is safe for JSON and CSV
    text = serialized_data.decode("utf-8")

    if method == "json":
        # json.loads does not execute code, so it is safe
        return json.loads(text)

    if method == "csv":
        # CSV is read into a list of dictionaries
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # The following line should never be reached due to the earlier check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")