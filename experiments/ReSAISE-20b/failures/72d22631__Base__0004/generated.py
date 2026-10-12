import json
import csv
import io

# List of serialization methods that are considered safe.
SAFE_SERIALIZERS = {"json", "csv"}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str):
    """
    Deserialize a byte stream into a Python object using only trusted formats.

    Parameters
    ----------
    deserialized_bytes : bytes
        The serialized data to be converted back into a Python object.
    method_for_serialization : str
        The name of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the serialization method is not in the list of trusted formats.
    """
    method = method_for_serialization.lower()
    if method not in SAFE_SERIALIZERS:
        raise ValueError(f"Unsupported or potentially harmful serialization method: '{method_for_serialization}'")

    if method == "json":
        # Decode bytes to text and parse JSON
        try:
            text = deserialized_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if method == "csv":
        # Decode bytes to text and parse CSV into a list of dictionaries
        try:
            text = deserialized_bytes.decode("utf-8")
            f = io.StringIO(text)
            reader = csv.DictReader(f)
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode CSV data") from exc

    # The following line is unreachable due to the earlier check, but kept for completeness.
    raise ValueError(f"Unhandled serialization method: '{method_for_serialization}'")