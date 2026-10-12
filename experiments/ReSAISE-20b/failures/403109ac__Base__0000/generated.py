import json
import csv
import io

# Allowed serialization formats – only safe, non-executable ones
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize `stream_bytes` according to `method_type`.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized data.
    method_type : str
        One of the allowed serialization formats ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `method_type` is not in the allowed set or if deserialization fails.
    """
    # Ensure the method is permitted
    if method_type not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type}")

    try:
        if method_type == "json":
            # json.loads expects a string, not bytes
            return json.loads(stream_bytes.decode("utf-8"))

        if method_type == "csv":
            # Use DictReader to return a list of dictionaries
            text_stream = io.StringIO(stream_bytes.decode("utf-8"))
            reader = csv.DictReader(text_stream)
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception from the deserialization libraries
        raise ValueError(f"Failed to deserialize using {method_type}: {exc}") from exc