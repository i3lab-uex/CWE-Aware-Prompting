import json
import csv
import io

# Define the set of serialization formats that are considered safe.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str):
    """
    Deserialize `encoded_bytes` using the specified serialization format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized data to be deserialized.
    format_name : str
        The name of the serialization format. Supported values are:
        - 'json'
        - 'csv'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the list of allowed formats or if
        deserialization fails.
    """
    if format_name not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name!r}")

    # Convert bytes to text using UTF-8.  This is safe because JSON and CSV are
    # text-based formats.
    try:
        text = encoded_bytes.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode bytes: {exc}") from exc

    if format_name == "json":
        try:
            return json.loads(text)
        except Exception as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    if format_name == "csv":
        try:
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"CSV deserialization error: {exc}") from exc

    # The above checks ensure we never reach this point.
    raise ValueError(f"Unhandled format: {format_name!r}")