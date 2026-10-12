import json
import csv
import io
from typing import Any

# A whitelist of safe deserialization methods.
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using a
    specified, whitelisted method.

    Parameters
    ----------
    data_stream : bytes
        The serialized data.
    deserialization_method : str
        One of the allowed serialization identifiers:
            - 'json'
            - 'csv'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not in the whitelist or if deserialization fails.
    """
    method = deserialization_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    try:
        if method == "json":
            # json.loads expects a str; decode bytes using UTF-8.
            return json.loads(data_stream.decode("utf-8"))

        if method == "csv":
            # csv.DictReader expects a text stream; wrap bytes with BytesIO and decode.
            stream = io.TextIOWrapper(io.BytesIO(data_stream), encoding="utf-8")
            reader = csv.DictReader(stream)
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into a ValueError to keep the public API consistent.
        raise ValueError(f"Deserialization failed for method '{deserialization_method}': {exc}") from exc