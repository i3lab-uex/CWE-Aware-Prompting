import json
import csv
import io
from typing import Any, List, Dict

# A whitelist of safe serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize `raw_data` according to the specified `format_type`.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    format_type : str
        The serialization format. Only formats listed in ALLOWED_FORMATS are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_type` is not in ALLOWED_FORMATS or if an insecure format (e.g. pickle)
        is requested.
    """
    fmt = format_type.lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or insecure serialization format: '{format_type}'. "
            f"Allowed formats are: {', '.join(sorted(ALLOWED_FORMATS))}."
        )

    text = raw_data.decode("utf-8")

    if fmt == "json":
        return json.loads(text)

    # format_type == "csv"
    reader = csv.DictReader(io.StringIO(text))
    result: List[Dict[str, str]] = [row for row in reader]
    return result