import json
import csv
import io
from typing import Any

# List of serialization formats that are considered safe.
TRUSTED_FORMATS = {"json", "csv"}


def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize ``serialized_data`` according to the specified
    ``deserialization_method`` while preventing insecure formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    deserialization_method : str
        One of the supported serialization formats, e.g. 'json', 'csv'.

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested method is not in :data:`TRUSTED_FORMATS` or if
        deserialization fails.
    """
    method = deserialization_method.lower()
    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")

    try:
        if method == "json":
            # JSON is text-based; decode bytes to str before parsing.
            return json.loads(serialized_data.decode("utf-8"))

        if method == "csv":
            # CSV is parsed into a list of dictionaries (one per row).
            text_stream = io.StringIO(serialized_data.decode("utf-8"))
            reader = csv.DictReader(text_stream)
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into a ValueError to avoid leaking low‑level details.
        raise ValueError(f"Deserialization error for method '{method}': {exc}") from exc