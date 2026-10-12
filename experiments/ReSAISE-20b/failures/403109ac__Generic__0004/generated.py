import json
import csv
from io import BytesIO, TextIOWrapper

# Set of serialization formats that are considered safe for deserialization
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize a byte stream into a Python object using the specified serialization format.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format used. Supported formats: 'json', 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or insecure serialization method is requested.
    """
    if method_type not in ALLOWED_METHODS:
        raise ValueError(
            f"Unsupported or insecure serialization method: {method_type!r}. "
            f"Allowed methods are: {', '.join(sorted(ALLOWED_METHODS))}."
        )

    if method_type == "json":
        # json.loads expects a str, so decode using UTF-8
        return json.loads(stream_bytes.decode("utf-8"))

    if method_type == "csv":
        # Use TextIOWrapper to read bytes as text
        buffer = BytesIO(stream_bytes)
        text_stream = TextIOWrapper(buffer, encoding="utf-8", newline="")
        reader = csv.reader(text_stream)
        # Convert the iterator to a list of rows
        return [row for row in reader]

    # The code should never reach here due to the ALLOWED_METHODS check
    raise RuntimeError("Unhandled serialization method")