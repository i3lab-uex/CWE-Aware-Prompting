import json
import csv
import io
from typing import Any, List, Dict

# A whitelist of safe serialization formats.  Only these are allowed.
_TRUSTED_FORMATS = {"json", "csv"}


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize a byte stream using only trusted serialization formats.

    Parameters
    ----------
    byte_data : bytes
        The raw data to deserialize.
    method_of_serialization : str
        Serialization format identifier (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `method_of_serialization` is not in the whitelist of trusted formats.
    TypeError
        If `byte_data` is not a bytes instance.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    method = method_of_serialization.lower()
    if method not in _TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or potentially unsafe serialization method: '{method_of_serialization}'. "
            f"Allowed methods are: {', '.join(sorted(_TRUSTED_FORMATS))}"
        )

    # Decode bytes to a string using UTF-8; errors='strict' ensures malformed data fails fast.
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Failed to decode byte data: {exc}") from exc

    if method == "json":
        # json.loads already returns a safe Python structure (dict, list, str, int, float, bool, None)
        return json.loads(text)

    if method == "csv":
        # Parse CSV into a list of dictionaries (header -> value).  No code execution occurs.
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached because of the whitelist check above.
    raise RuntimeError("Unhandled serialization method")  # pragma: no cover