import json
import csv
from io import BytesIO, TextIOWrapper

# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "csv"}


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str):
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    deserialized_bytes : bytes
        The raw byte stream to be deserialized.
    method_for_serialization : str
        Name of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    fmt = method_for_serialization.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {method_for_serialization}")

    # JSON deserialization
    if fmt == "json":
        try:
            text = deserialized_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON") from exc

    # CSV deserialization
    if fmt == "csv":
        try:
            with BytesIO(deserialized_bytes) as buffer:
                # csv module expects text, so wrap the bytes with a TextIOWrapper
                text_stream = TextIOWrapper(buffer, encoding="utf-8")
                reader = csv.DictReader(text_stream)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV") from exc

    # In practice this point is unreachable due to the earlier check
    raise ValueError(f"Unhandled serialization format: {method_for_serialization}")