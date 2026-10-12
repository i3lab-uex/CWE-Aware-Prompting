import json
import csv
from io import BytesIO, TextIOWrapper

# List of trusted serialization formats
_TRUSTED_METHODS = {"json", "csv"}


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str):
    """
    Recover a Python object from serialized data.

    Parameters
    ----------
    deserialized_bytes : bytes
        The byte stream containing the serialized data.
    method_for_serialization : str
        The serialization format used. Supported formats are 'json' and 'csv'.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If an unsupported or potentially harmful serialization method is requested.
    """
    method = method_for_serialization.lower()

    if method not in _TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or potentially unsafe serialization method: {method_for_serialization}"
        )

    if method == "json":
        # JSON is safe for deserialization as long as it only contains data.
        try:
            text = deserialized_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # CSV is treated as a list of dictionaries.
        try:
            with BytesIO(deserialized_bytes) as bio, TextIOWrapper(bio, encoding="utf-8") as txt:
                reader = csv.DictReader(txt)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc

    # The code should never reach here because of the earlier check.
    raise ValueError(f"Unhandled serialization method: {method_for_serialization}")