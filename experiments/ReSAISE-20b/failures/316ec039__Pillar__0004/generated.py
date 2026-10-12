import json
import csv
from io import StringIO, TextIOWrapper

def load_object(serialized_data: bytes, deserialization_method: str):
    """
    Restore a Python object from serialized byte data using only
    trusted serialization methods.

    Supported formats:
        - 'json' : JSON format (safe)
        - 'csv'  : CSV format, returns a list of dicts

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream to deserialize.
    deserialization_method : str
        Identifier of the serialization format.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in the whitelist or if
        deserialization fails.
    """
    # Whitelist of safe methods
    _SAFE_METHODS = {"json", "csv"}

    method = deserialization_method.lower()
    if method not in _SAFE_METHODS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")

    try:
        if method == "json":
            # JSON can be safely loaded with json.loads
            text = serialized_data.decode("utf-8")
            return json.loads(text)

        if method == "csv":
            # Decode bytes to text and parse as CSV
            text_stream = StringIO(serialized_data.decode("utf-8"))
            reader = csv.DictReader(text_stream)
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into ValueError to avoid leaking implementation details
        raise ValueError(f"Deserialization failed for method {deserialization_method}: {exc}") from exc