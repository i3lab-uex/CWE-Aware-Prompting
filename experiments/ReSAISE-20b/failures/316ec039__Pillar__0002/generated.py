import json
import csv
from io import BytesIO
from typing import Any

# List of trusted serialization formats
TRUSTED_METHODS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize `serialized_data` according to the specified method.
    
    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized object.
    deserialization_method : str
        The name of the serialization format (e.g., 'json', 'csv').
    
    Returns
    -------
    Any
        The deserialized Python object.
    
    Raises
    ------
    ValueError
        If the method is not trusted or unsupported.
    """
    if deserialization_method.lower() not in TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")

    # Use a context manager to ensure the BytesIO buffer is closed
    with BytesIO(serialized_data) as stream:
        if deserialization_method.lower() == "json":
            # Decode bytes to string (UTF-8 is the common default)
            text = stream.read().decode("utf-8")
            return json.loads(text)

        elif deserialization_method.lower() == "csv":
            # Use csv.DictReader to parse CSV into a list of dictionaries
            text_stream = stream.read().decode("utf-8").splitlines()
            reader = csv.DictReader(text_stream)
            return [row for row in reader]

    # The code should never reach here because all trusted methods are handled
    raise ValueError("Unhandled deserialization method")