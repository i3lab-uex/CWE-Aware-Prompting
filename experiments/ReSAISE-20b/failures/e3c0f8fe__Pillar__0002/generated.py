import json
import csv
from io import BytesIO, TextIOWrapper

# Registry of trusted serialization methods
ALLOWED_METHODS = {
    "json": "json",
    "csv": "csv",
}

def restore_object(serialized_bytes: bytes, serialization_method: str):
    """
    Deserialize a Python object from a byte stream using only trusted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `serialization_method` is not in the list of allowed methods.
    """
    method = ALLOWED_METHODS.get(serialization_method.lower())
    if not method:
        raise ValueError(f"Unsupported or insecure serialization method: {serialization_method}")

    try:
        if method == "json":
            # JSON is safe for text data
            decoded = serialized_bytes.decode("utf-8")
            return json.loads(decoded)

        if method == "csv":
            # CSV is interpreted as text; returns a list of dicts
            stream = TextIOWrapper(BytesIO(serialized_bytes), encoding="utf-8")
            reader = csv.DictReader(stream)
            return [row for row in reader]

    except Exception as exc:
        # Wrap any deserialization error to avoid leaking implementation details
        raise ValueError(f"Failed to deserialize using {serialization_method}: {exc}") from exc