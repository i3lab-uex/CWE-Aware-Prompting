import json
import csv
from io import StringIO
from typing import Any

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using
    only authorized, safe serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The byte stream containing the serialized data.
    method_of_serialization : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is disallowed or not recognized.
    """
    if method_of_serialization not in SAFE_METHODS:
        raise ValueError(f"Disallowed or unknown serialization method: "
                         f"{method_of_serialization!r}")

    # Ensure data is text for json and csv
    try:
        text_data = data_bytes_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF‑8 text") from exc

    if method_of_serialization == "json":
        # Use json.loads; it only constructs basic Python types
        return json.loads(text_data)

    if method_of_serialization == "csv":
        # Parse CSV into a list of dictionaries
        reader = csv.DictReader(StringIO(text_data))
        return [row for row in reader]

    # The code should never reach here because of the earlier check
    raise ValueError(f"Unhandled serialization method: {method_of_serialization!r}")