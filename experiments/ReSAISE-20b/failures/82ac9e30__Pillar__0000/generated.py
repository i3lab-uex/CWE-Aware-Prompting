import json
import csv
from io import StringIO
from typing import Any


# List of serialization methods that are considered safe for deserialization.
SAFE_METHODS = {"json", "csv"}


def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only approved methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized data as a byte string.
    deserialization_method : str
        Identifier of the serialization format used. Supported values are
        'json' and 'csv'.

    Returns
    -------
    Any
        The Python object produced by deserialization.

    Raises
    ------
    ValueError
        If the requested method is not recognized or is disallowed.
    """
    # Normalise the method name
    method = deserialization_method.strip().lower()

    if method not in SAFE_METHODS:
        raise ValueError(
            f"Deserialization method '{deserialization_method}' is not allowed."
        )

    # Decode bytes to string safely
    try:
        text = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream is not valid UTF-8.") from exc

    if method == "json":
        # json.loads is safe for simple data structures (dict, list, str, int, float, bool, None)
        return json.loads(text)

    if method == "csv":
        # Return a list of dictionaries, one per row.
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")