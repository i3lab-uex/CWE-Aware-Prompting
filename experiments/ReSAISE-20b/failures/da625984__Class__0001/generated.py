import json
import csv
import io
from typing import Any, List, Dict


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize a byte stream using only trusted serialization formats.

    Supported methods:
        - 'json': JSON format.
        - 'csv' : CSV format (returns a list of dictionaries).

    Parameters
    ----------
    byte_data : bytes
        The data stream to be deserialized.
    method_of_serialization : str
        The serialization format of the data.

    Returns
    -------
    Any
        The Python object recovered from the serialized byte stream.

    Raises
    ------
    ValueError
        If an unsupported or potentially harmful serialization method is requested.
    """
    # Define the set of allowed, secure serialization methods
    TRUSTED_METHODS = {"json", "csv"}

    method = method_of_serialization.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or potentially unsafe serialization method: {method_of_serialization}"
        )

    if method == "json":
        # JSON deserialization – always safe for primitive data structures
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte data is not valid UTF-8 for JSON") from exc
        return json.loads(text)

    # CSV deserialization – safe as it only parses plain text into lists/dicts
    if method == "csv":
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte data is not valid UTF-8 for CSV") from exc

        # Use StringIO to treat the string as a file-like object
        csv_file = io.StringIO(text)
        reader = csv.DictReader(csv_file)
        return [row for row in reader]

    # The code should never reach here because of the earlier check
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")