import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a Python object from a byte stream using a trusted method.

    Parameters
    ----------
    serialized_data : bytes
        The data stream to be deserialized.
    deserialization_method : str
        Specifies the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object recovered from the serialized byte stream.

    Raises
    ------
    ValueError
        If an unsupported or potentially harmful serialization method is requested.
    """
    if not isinstance(serialized_data, bytes):
        raise TypeError("serialized_data must be of type 'bytes'")

    method = deserialization_method.lower()
    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization method: '{deserialization_method}'")

    if method == "json":
        # Decode bytes to string safely; errors='strict' will raise on invalid UTF‑8
        text = serialized_data.decode("utf-8")
        return json.loads(text)

    if method == "csv":
        # Use TextIOWrapper to provide a text stream for csv module
        with TextIOWrapper(BytesIO(serialized_data), encoding="utf-8") as text_stream:
            reader = csv.DictReader(text_stream)
            # Convert the iterator to a list of dictionaries
            return [row for row in reader]

    # This point should never be reached because of the earlier check
    raise ValueError(f"Unhandled deserialization method: '{deserialization_method}'")