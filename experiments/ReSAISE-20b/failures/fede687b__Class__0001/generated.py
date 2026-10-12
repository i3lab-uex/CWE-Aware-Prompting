import json
import csv
import io

# Whitelisted serialization formats that are considered safe for deserialization
SAFE_FORMATS = {"json", "csv"}


def deserialize_object(raw_data: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object using the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized input data.
    format_type : str
        One of the supported serialization formats ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.  For JSON it will be a native Python data
        structure (dict, list, etc.).  For CSV it returns a list of dictionaries,
        one per row.

    Raises
    ------
    ValueError
        If the format_type is not in the whitelist or if deserialization fails.
    """
    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    try:
        if fmt == "json":
            # JSON is safe as long as we use the json module and avoid eval
            return json.loads(raw_data.decode("utf-8"))

        if fmt == "csv":
            # Convert bytes to text and parse as CSV
            csv_text = raw_data.decode("utf-8")
            reader = csv.DictReader(io.StringIO(csv_text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception from the underlying libraries
        raise ValueError(f"Failed to deserialize {format_type} data: {exc}") from exc