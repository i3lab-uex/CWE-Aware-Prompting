import json
import csv
from io import BytesIO

# Registry of allowed serialization methods
ALLOWED_METHODS = {
    "json": "json",
    "csv": "csv",
}

def restore_object(serialized_bytes: bytes, serialization_method: str):
    """
    Restore a Python object from serialized data.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw data to deserialize.
    serialization_method : str
        Identifier of the serialization format. Supported values are:
        - 'json'
        - 'csv'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not supported or considered insecure.
    """
    method = ALLOWED_METHODS.get(serialization_method.lower())
    if method is None:
        raise ValueError(f"Unsupported or insecure serialization method: {serialization_method}")

    if method == "json":
        # JSON is safe as it only creates basic Python types
        return json.loads(serialized_bytes.decode("utf-8"))

    if method == "csv":
        # CSV is treated as a list of dictionaries (row → column mapping)
        decoded = serialized_bytes.decode("utf-8")
        reader = csv.DictReader(decoded.splitlines())
        return [row for row in reader]

    # This point should never be reached because of the registry check
    raise ValueError(f"Unhandled serialization method: {serialization_method}")