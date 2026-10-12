import json
import csv
from io import StringIO, BytesIO
from typing import Any

# Define the set of serialization methods that are considered safe
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream using the specified serialization format.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The name of the serialization format to use.  Only values in
        `ALLOWED_METHODS` are permitted.

    Returns
    -------
    Any
        The deserialized Python object.  For JSON it is the parsed value.
        For CSV it returns a list of dictionaries, one per row.

    Raises
    ------
    ValueError
        If `method_type` is not in the allowed set or if deserialization fails.
    """
    method = method_type.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type}")

    try:
        if method == "json":
            # json.loads expects a str, so decode assuming UTF-8
            return json.loads(stream_bytes.decode("utf-8"))

        if method == "csv":
            # Treat the stream as UTF‑8 encoded CSV text
            text = stream_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception from the underlying parser in a ValueError
        raise ValueError(f"Failed to deserialize data using {method_type}: {exc}") from exc