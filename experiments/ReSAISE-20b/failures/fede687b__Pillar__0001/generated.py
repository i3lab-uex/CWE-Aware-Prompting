import json
import csv
from io import BytesIO, TextIOWrapper

# Allowed serialization formats
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str):
    """
    Deserialize `raw_data` according to the specified `format_type`.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        Serialization format used. Allowed values are 'json' and 'csv'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_type` is not supported or if deserialization fails.
    """
    format_type = format_type.lower()
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization method: {format_type}")

    # JSON deserialization
    if format_type == "json":
        try:
            # Decode bytes to string assuming UTF-8
            text = raw_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    # CSV deserialization
    if format_type == "csv":
        try:
            with BytesIO(raw_data) as bio:
                # CSV library expects a text stream; wrap BytesIO with TextIOWrapper
                with TextIOWrapper(bio, encoding="utf-8") as text_stream:
                    reader = csv.DictReader(text_stream)
                    # Convert to list of dictionaries
                    return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"CSV deserialization error: {exc}") from exc