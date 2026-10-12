import json
import csv
from io import BytesIO, TextIOWrapper

# Define the set of allowed serialization formats.
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format used. Supported values are:
            - 'json'
            - 'csv'

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method_type is not in ALLOWED_METHODS or if deserialization fails.
    """
    # Normalise method_type to lower case and validate it
    fmt = method_type.lower()
    if fmt not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: '{method_type}'")

    try:
        if fmt == "json":
            # json.loads expects a str; decode using UTF-8
            return json.loads(stream_bytes.decode("utf-8"))

        elif fmt == "csv":
            # Use csv.DictReader to produce a list of dictionaries
            with BytesIO(stream_bytes) as bio:
                # Wrap the binary stream in a text wrapper for csv
                with TextIOWrapper(bio, encoding="utf-8") as txt:
                    reader = csv.DictReader(txt)
                    return [row for row in reader]

    except Exception as exc:
        # Re‑raise as ValueError to indicate deserialization failure
        raise ValueError(f"Failed to deserialize using method '{method_type}': {exc}") from exc