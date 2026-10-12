import json
import csv
from io import TextIOWrapper, BytesIO
from typing import Any


# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}


def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Safely deserialize `serialized_data` using the specified method.

    Parameters
    ----------
    serialized_data : bytes
        The raw data stream to deserialize.
    deserialization_method : str
        The name of the serialization format ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in the trusted list or if deserialization fails.
    """
    method = deserialization_method.lower()
    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or potentially harmful deserialization method: {deserialization_method}")

    try:
        if method == "json":
            # Decode bytes to string safely
            text = serialized_data.decode("utf-8")
            return json.loads(text)

        elif method == "csv":
            # Decode bytes to text and parse CSV
            with BytesIO(serialized_data) as bio:
                # TextIOWrapper provides text interface to binary stream
                with TextIOWrapper(bio, encoding="utf-8", newline="") as txt:
                    reader = csv.DictReader(txt)
                    return [row for row in reader]

    except (json.JSONDecodeError, csv.Error) as exc:
        raise ValueError(f"Deserialization failed for method '{deserialization_method}': {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"Failed to decode bytes for method '{deserialization_method}': {exc}") from exc