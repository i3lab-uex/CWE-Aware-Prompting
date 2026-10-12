import json
import csv
from io import StringIO, BytesIO

# Whitelisted serialization methods – only safe formats are allowed
ALLOWED_METHODS = {
    "json",
    "csv",
}

def restore_object(serialized_bytes: bytes, serialization_method: str):
    """
    Deserialize a Python object from a byte stream.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw data to deserialize.
    serialization_method : str
        Identifier of the serialization format used.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not in the whitelist or if data
        cannot be parsed by the chosen format.
    """
    method = serialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    try:
        if method == "json":
            # JSON is safe – it only creates basic Python data structures
            return json.loads(serialized_bytes.decode("utf-8"))

        if method == "csv":
            # Convert CSV bytes to a string and parse into list of dicts
            text = serialized_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any parsing errors in a ValueError to keep the API simple
        raise ValueError(f"Failed to deserialize using {serialization_method}: {exc}") from exc