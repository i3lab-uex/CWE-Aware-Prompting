import json
import csv
from io import BytesIO
from typing import Any, List, Dict

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Restore a Python object from serialized bytes using only trusted
    serialization formats.

    Parameters
    ----------
    deserialized_bytes : bytes
        The byte stream containing the serialized data.
    method_for_serialization : str
        The serialization format used. Supported values are:
        - 'json'
        - 'csv'

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `method_for_serialization` is not a supported or safe format.
    """
    # Normalise the method name to lower case
    method = method_for_serialization.strip().lower()

    if method == 'json':
        # JSON is safe for basic data structures
        try:
            text = deserialized_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method == 'csv':
        # CSV is safe but only produces simple data structures.
        try:
            text = deserialized_bytes.decode('utf-8')
            f = BytesIO(deserialized_bytes)
            reader = csv.DictReader(BytesIO(text.encode('utf-8')))
            # Return list of dicts; each row is a dict
            return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"Invalid CSV data: {exc}") from exc

    # If we reach here, the method is unsupported or potentially unsafe
    raise ValueError(f"Unsupported serialization format: {method_for_serialization!r}")