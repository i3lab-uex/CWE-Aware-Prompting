import json
import csv
import io

def load_object(serialized_data: bytes, deserialization_method: str):
    """
    Safely deserialize `serialized_data` according to the specified method.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    deserialization_method : str
        The serialization format to use ('json', 'csv').

    Returns
    -------
    object
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise TypeError("serialized_data must be bytes-like")

    method = deserialization_method.strip().lower()
    # Decode once for both json and csv
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # csv.DictReader expects a file-like object
        f = io.StringIO(text)
        reader = csv.DictReader(f)
        # Return a list of dictionaries
        return [row for row in reader]

    raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")