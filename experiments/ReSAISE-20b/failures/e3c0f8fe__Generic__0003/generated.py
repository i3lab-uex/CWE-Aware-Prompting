import json
import csv
from io import BytesIO, TextIOWrapper

# Registry of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}

def restore_object(serialized_bytes: bytes, serialization_method: str):
    """
    Restore a Python object from a serialized byte stream.

    Parameters
    ----------
    serialized_bytes : bytes
        The data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format (e.g. 'json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unrecognized or insecure.
    """
    if serialization_method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    # Common decoding step
    text_stream = TextIOWrapper(BytesIO(serialized_bytes), encoding="utf-8")

    if serialization_method == "json":
        # json.loads expects a str, not a stream
        return json.load(text_stream)

    if serialization_method == "csv":
        # csv.DictReader returns an iterator; convert to a list
        reader = csv.DictReader(text_stream)
        return [row for row in reader]

    # In practice this point is unreachable due to the allowed set
    raise ValueError(f"Unhandled serialization method: {serialization_method}")