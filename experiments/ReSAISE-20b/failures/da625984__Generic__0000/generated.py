import json
import csv
from io import StringIO
from typing import Any


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Restore a Python object from a byte stream using only trusted
    serialization methods.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    method_of_serialization : str
        The serialization format. Supported values are:
            - 'json'  : JSON encoded data.
            - 'csv'   : CSV encoded data (returns a list of dictionaries).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested serialization method is unsupported or potentially
        unsafe.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    method = method_of_serialization.lower()

    if method == "json":
        # JSON is safe for data-only structures
        return json.loads(byte_data.decode("utf-8"))

    if method == "csv":
        # CSV is safe for data-only structures
        text = byte_data.decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # Any other method is considered unsafe or unsupported
    raise ValueError(f"Unsupported or potentially harmful serialization method: {method_of_serialization}")