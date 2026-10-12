import json
import csv
import io
from typing import Any, List, Dict


# --------------------------------------------------------------------------- #
# Trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}  # only these are allowed


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only trusted
    serialization methods.

    Parameters
    ----------
    deserialized_bytes : bytes
        The serialized data.
    method_for_serialization : str
        Serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    # Normalize the method name
    fmt = method_for_serialization.strip().lower()

    if fmt not in TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization method: '{method_for_serialization}'. "
            f"Allowed methods are: {', '.join(sorted(TRUSTED_FORMATS))}"
        )

    # Decode the bytes to a string (UTF-8 is standard for json/csv)
    try:
        text = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # Read CSV into a list of dictionaries
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # Should never reach here because of the earlier check
    raise ValueError(f"Unhandled serialization method: {method_for_serialization}")