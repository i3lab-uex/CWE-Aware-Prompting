import json
import csv
from io import StringIO, BytesIO
from typing import Any

# A whitelist of serialization formats that are considered safe.
SAFE_SERIALIZERS = {
    "json",
    "csv",
}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Safely reconstruct a Python object from serialized bytes.

    Parameters
    ----------
    deserialized_bytes : bytes
        The byte stream containing the serialized data.
    method_for_serialization : str
        The serialization format used. Must be one of the keys in
        SAFE_SERIALIZERS.

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `method_for_serialization` is not in the whitelist or if the data
        cannot be parsed using the chosen method.
    """
    # Normalise the format name and check against the whitelist
    fmt = method_for_serialization.strip().lower()
    if fmt not in SAFE_SERIALIZERS:
        raise ValueError(f"Unsupported or unsafe serialization method: {fmt}")

    # Ensure we have a text stream for formats that expect text
    try:
        if fmt == "json":
            # json.loads expects a string, not bytes
            text = deserialized_bytes.decode("utf-8")
            return json.loads(text)

        if fmt == "csv":
            # csv module works with text; decode and wrap in StringIO
            text = deserialized_bytes.decode("utf-8")
            f = StringIO(text)
            reader = csv.DictReader(f)
            # Return a list of dictionaries (each row as a dict)
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception from the parsing libraries
        raise ValueError(f"Failed to deserialize using {fmt}: {exc}") from exc

    # This point should never be reached because all whitelisted formats
    # are handled above.  The following is defensive programming.
    raise ValueError(f"Unhandled serialization format: {fmt}")