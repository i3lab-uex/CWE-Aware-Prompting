import json
import csv
import io

# Allowed serialization formats (safe ones only)
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str):
    """
    Deserialize raw data into a Python object using the specified format.

    Parameters
    ----------
    raw_data : bytes
        Serialized input data.
    format_type : str
        The serialization format used ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is unsupported or considered insecure.
    """
    if not isinstance(raw_data, (bytes, bytearray)):
        raise TypeError("raw_data must be bytes or bytearray")

    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    try:
        if fmt == "json":
            # JSON is safe when loaded into basic Python types
            text = raw_data.decode("utf-8")
            return json.loads(text)

        elif fmt == "csv":
            # CSV is treated as a list of dictionaries
            text = raw_data.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any parsing exception into a ValueError to avoid leaking internal details
        raise ValueError(f"Failed to deserialize data as {format_type}: {exc}") from exc