import json
import csv
from io import BytesIO, TextIOWrapper

# Define the set of allowed serialization formats.
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize a byte stream into a Python object using only approved formats.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

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
            # json.loads expects a string, so decode using UTF-8.
            return json.loads(stream_bytes.decode("utf-8"))
        elif method == "csv":
            # CSV is read as text. Use TextIOWrapper to decode the bytes.
            with BytesIO(stream_bytes) as bio:
                text_stream = TextIOWrapper(bio, encoding="utf-8")
                reader = csv.DictReader(text_stream)
                return [row for row in reader]
    except Exception as exc:
        # Wrap any exception into a ValueError to avoid leaking implementation details.
        raise ValueError(f"Failed to deserialize stream using {method_type}: {exc}") from exc