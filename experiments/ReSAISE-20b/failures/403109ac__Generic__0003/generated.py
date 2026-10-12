import json
import csv
from io import StringIO
from typing import Any

# Whitelisted serialization methods – only safe, non-executable formats are allowed
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format used, e.g. 'json', 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified method is not in the whitelist or if deserialization fails.
    """
    # Normalise and validate the method name
    method = method_type.strip().lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: '{method_type}'")

    try:
        if method == "json":
            # json.loads expects a string, so decode using UTF-8
            return json.loads(stream_bytes.decode("utf-8"))

        if method == "csv":
            # CSV is interpreted as a list of dictionaries
            text = stream_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any deserialization exception into a ValueError for clarity
        raise ValueError(f"Failed to deserialize stream using '{method_type}': {exc}") from exc