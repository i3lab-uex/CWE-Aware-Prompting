import json
import csv
import io

# Define the set of serialization methods that are explicitly allowed.
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize a byte stream using the specified serialization format.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized data.
    method_type : str
        The serialization format used. Must be one of the allowed methods.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in the list of allowed methods or if
        deserialization fails.
    """
    # Normalise the method name to lower case for comparison.
    fmt = method_type.strip().lower()

    if fmt not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type!r}")

    try:
        if fmt == "json":
            # json.loads expects a string, so decode using UTF-8.
            return json.loads(stream_bytes.decode("utf-8"))

        if fmt == "csv":
            # CSV is text based; decode bytes and read via csv.DictReader.
            decoded = stream_bytes.decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded))
            # Return a list of rows, each row is an OrderedDict.
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception in a ValueError to keep the API consistent.
        raise ValueError(f"Failed to deserialize using {method_type!r}: {exc}") from exc