import json
import csv
import io
from typing import Any

# List of trusted serialization formats
TRUSTED_METHODS = {"json", "csv"}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Restore a Python object from serialized bytes using a trusted method.

    Parameters
    ----------
    deserialized_bytes : bytes
        The serialized data stream.
    method_for_serialization : str
        Serialization format: 'json' or 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unsupported or potentially unsafe.
    """
    # Normalise method name to lower case for comparison
    method = method_for_serialization.lower()

    if method not in TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported serialization method: '{method_for_serialization}'. "
            "Only 'json' and 'csv' are allowed."
        )

    # Decode bytes to string (assuming UTF-8 encoding)
    try:
        data_str = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded text.") from exc

    if method == "json":
        # Use json.loads which is safe for standard JSON data
        return json.loads(data_str)

    if method == "csv":
        # Interpret CSV as a list of dictionaries (one per row)
        csv_file = io.StringIO(data_str)
        reader = csv.DictReader(csv_file)
        return [row for row in reader]

    # Should never reach here due to earlier check
    raise ValueError(f"Unhandled method: {method}")