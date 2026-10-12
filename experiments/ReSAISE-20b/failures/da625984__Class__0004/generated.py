import json
import csv
from io import BytesIO, TextIOWrapper

def deserialize_obj(byte_data: bytes, method_of_serialization: str):
    """
    Restore a Python object from serialized byte data.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    method_of_serialization : str
        Serialization format identifier (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    # Define a whitelist of safe, trusted formats
    SAFE_METHODS = {"json", "csv"}

    method = method_of_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: {method_of_serialization}"
        )

    if method == "json":
        # Decode bytes to string using UTF-8 (common default for JSON)
        text = byte_data.decode("utf-8")
        return json.loads(text)

    if method == "csv":
        # CSV is read into a list of dictionaries (first row as header)
        with BytesIO(byte_data) as bio:
            # Use TextIOWrapper to provide text interface over bytes
            with TextIOWrapper(bio, encoding="utf-8") as txt:
                reader = csv.DictReader(txt)
                return list(reader)

    # The code should never reach here because of the whitelist check
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")