import json
import csv
from io import BytesIO, TextIOWrapper

# List of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into its corresponding Python object using only
    authorized, safe serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data.
    method_of_serialization : str
        The name of the serialization method used ("json", "csv").

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not in SAFE_METHODS or if deserialization fails.
    """
    method = method_of_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed.")

    try:
        if method == "json":
            # json.loads expects a string, so decode UTF‑8
            return json.loads(data_bytes_stream.decode("utf-8"))
        elif method == "csv":
            # csv.DictReader expects a text stream
            with TextIOWrapper(BytesIO(data_bytes_stream), encoding="utf-8") as text_file:
                reader = csv.DictReader(text_file)
                return [row for row in reader]
    except Exception as exc:
        raise ValueError(f"Failed to deserialize data using method '{method_of_serialization}': {exc}") from exc