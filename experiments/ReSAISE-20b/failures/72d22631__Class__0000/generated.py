import json
import csv
import io
from typing import Any, Union


def recover_obj(deserialized_bytes: bytes,
                method_for_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    trusted serialization formats.

    Parameters
    ----------
    deserialized_bytes : bytes
        The byte stream to deserialize.
    method_for_serialization : str
        The name of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    # Define a whitelist of safe formats
    TRUSTED_METHODS = {"json", "csv"}

    method = method_for_serialization.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe serialization format: "
                         f"{method_for_serialization}")

    # Decode bytes to text (UTF-8 is a common default)
    try:
        text = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF-8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # CSV handling: returns a list of dictionaries (first row as headers)
    if method == "csv":
        reader = csv.DictReader(io.StringIO(text))
        return list(reader)

    # In practice we should never reach here because of the whitelist,
    # but keep a fallback for defensive programming.
    raise ValueError(f"Unhandled serialization method: {method}")