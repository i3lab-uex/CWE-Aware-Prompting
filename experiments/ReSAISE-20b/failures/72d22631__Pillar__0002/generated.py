import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# List of trusted serialization formats.
TRUSTED_METHODS = {"json", "csv"}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only trusted methods.

    Parameters
    ----------
    deserialized_bytes : bytes
        The serialized data to be recovered.
    method_for_serialization : str
        Serialization format: 'json' or 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    if not isinstance(deserialized_bytes, bytes):
        raise ValueError("Input must be of type 'bytes'.")

    method = method_for_serialization.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe serialization method: '{method_for_serialization}'")

    if method == "json":
        # json.loads expects a string; decode bytes safely using UTF-8
        text = deserialized_bytes.decode("utf-8")
        return json.loads(text)

    if method == "csv":
        # Parse CSV into a list of dictionaries (first row as headers)
        with TextIOWrapper(BytesIO(deserialized_bytes), encoding="utf-8") as text_file:
            reader = csv.DictReader(text_file)
            return [row for row in reader]

    # This point should never be reached due to the whitelist check.
    raise ValueError(f"Unhandled serialization method: '{method_for_serialization}'")