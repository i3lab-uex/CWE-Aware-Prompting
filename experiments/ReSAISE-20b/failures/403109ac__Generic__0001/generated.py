import json
import csv
from io import BytesIO, TextIOWrapper

# Allowed serialization formats (security‑safe)
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize a byte stream into a Python object using the specified
    serialization format.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        Serialization format identifier ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object (e.g. dict, list).

    Raises
    ------
    ValueError
        If the method_type is not in ALLOWED_METHODS or if deserialization fails.
    """
    method = method_type.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type}")

    try:
        if method == "json":
            # Decode bytes to string and parse JSON
            return json.loads(stream_bytes.decode("utf-8"))

        elif method == "csv":
            # Use TextIOWrapper to decode bytes as UTF‑8 text for csv.reader
            with TextIOWrapper(BytesIO(stream_bytes), encoding="utf-8") as text_file:
                reader = csv.DictReader(text_file)
                return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into a ValueError to keep the API simple
        raise ValueError(f"Failed to deserialize data with method '{method_type}': {exc}") from exc