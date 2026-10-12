import json
import csv
import io

# List of safe serialization methods that are allowed for deserialization
SAFE_SERIALIZERS = {
    'json',
    'csv',   # CSV is allowed but parsed as a list of dictionaries
}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data in byte form.
    format_method : str
        The serialization method used. Supported values are:
            - 'json'   -> Python object (dict, list, etc.)
            - 'csv'    -> List of dictionaries representing rows.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_method is not in SAFE_SERIALIZERS or not recognized.
    """
    method = format_method.lower()
    if method not in SAFE_SERIALIZERS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or recognized.")

    # Common decoding step for all supported formats
    try:
        text = data_bytes.decode('utf-8')
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to decode bytes using UTF-8.") from exc

    if method == 'json':
        # JSON deserialization is safe as long as the input is trusted
        return json.loads(text)

    if method == 'csv':
        # Parse CSV into a list of dictionaries
        f = io.StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # The above guard ensures we never reach this point,
    # but this is a defensive fallback.
    raise ValueError(f"Unhandled serialization method: {format_method}")