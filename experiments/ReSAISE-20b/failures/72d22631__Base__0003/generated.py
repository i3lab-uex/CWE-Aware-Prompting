import json
import csv
import io
from typing import Any


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Safely deserialize a byte stream that was serialized using one of the
    supported, trusted formats.

    Supported formats:
        - 'json'  : JSON format (text based).
        - 'csv'   : CSV format (comma separated values).  Returns a list of
                    dictionaries, one per row.

    Parameters
    ----------
    deserialized_bytes : bytes
        The raw byte stream to be decoded.
    method_for_serialization : str
        Identifier of the serialization format.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially unsafe.
    """
    # Define a whitelist of safe, supported formats
    SAFE_FORMATS = {"json", "csv"}

    method = method_for_serialization.lower()
    if method not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization method: '{method_for_serialization}'. "
            f"Only the following formats are allowed: {', '.join(SAFE_FORMATS)}."
        )

    # Decode bytes to text (UTF‑8 is a common default for textual formats)
    try:
        text = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "The provided byte stream could not be decoded as UTF‑8."
        ) from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if method == "csv":
        # Use csv.DictReader to parse rows into dictionaries
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # The above guard ensures we never reach this point,
    # but return None as a defensive fallback.
    return None