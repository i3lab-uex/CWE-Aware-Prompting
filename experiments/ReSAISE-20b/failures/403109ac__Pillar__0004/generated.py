import json
import csv
from io import BytesIO, TextIOWrapper

# Whitelist of safe serialization formats
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str):
    """
    Deserialize a byte stream using the specified serialization format.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        One of the allowed serialization methods: 'json' or 'csv'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the method_type is not in ALLOWED_METHODS or if deserialization fails.
    """
    # Validate the requested method
    if method_type not in ALLOWED_METHODS:
        raise ValueError(
            f"Unsupported or insecure serialization method: {method_type!r}"
        )

    try:
        if method_type == "json":
            # JSON expects text; decode using UTF-8
            return json.loads(stream_bytes.decode("utf-8"))

        elif method_type == "csv":
            # CSV is text-based; parse into a list of dictionaries
            with BytesIO(stream_bytes) as bio:
                # Wrap the binary stream in a text wrapper for csv
                with TextIOWrapper(bio, encoding="utf-8") as txt:
                    reader = csv.DictReader(txt)
                    return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into a ValueError to avoid leaking internal details
        raise ValueError(f"Failed to parse stream as {method_type}") from exc