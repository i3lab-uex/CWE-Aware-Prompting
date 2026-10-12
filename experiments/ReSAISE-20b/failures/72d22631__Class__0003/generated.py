import json
import csv
import io
from typing import Any


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Restore a Python object from serialized bytes using only trusted serialization methods.

    Parameters
    ----------
    deserialized_bytes : bytes
        The byte stream containing the serialized data.
    method_for_serialization : str
        The name of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the requested serialization method is not trusted or supported.
    """
    # Define a whitelist of safe serialization formats
    SAFE_METHODS = {"json", "csv"}

    method = method_for_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(
            f"Unsupported or potentially dangerous serialization method: {method_for_serialization}"
        )

    if method == "json":
        # JSON is safe as it only constructs basic Python data types
        return json.loads(deserialized_bytes.decode("utf-8"))

    if method == "csv":
        # CSV is safe; we parse into a list of dictionaries
        text_stream = io.StringIO(deserialized_bytes.decode("utf-8"))
        reader = csv.DictReader(text_stream)
        return [row for row in reader]

    # In practice this point is unreachable because of the whitelist,
    # but we keep it for completeness.
    raise ValueError(f"Unhandled serialization method: {method}")