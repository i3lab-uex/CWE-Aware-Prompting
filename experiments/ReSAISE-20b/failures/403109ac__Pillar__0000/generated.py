import json
import csv
from io import BytesIO, TextIOWrapper, StringIO

# Define the set of allowed serialization methods.
ALLOWED_METHODS = {"json", "csv"}  # Pickle and other binary formats are intentionally excluded.


def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize a byte stream into a Python object using the specified serialization format.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format to use (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method_type is not in ALLOWED_METHODS or if deserialization fails.
    """
    # Normalise the method type for case-insensitive comparison
    fmt = method_type.lower()

    if fmt not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type!r}")

    try:
        if fmt == "json":
            # json.loads expects a str; decode using UTF-8
            return json.loads(stream_bytes.decode("utf-8"))

        if fmt == "csv":
            # CSV is textual; wrap the bytes in a TextIOWrapper for proper decoding
            with TextIOWrapper(BytesIO(stream_bytes), encoding="utf-8") as text_stream:
                reader = csv.reader(text_stream)
                # Return all rows as a list of lists
                return [row for row in reader]

    except Exception as exc:
        # Wrap any exception from the deserialization library
        raise ValueError(f"Failed to deserialize stream using {method_type!r}: {exc}") from exc