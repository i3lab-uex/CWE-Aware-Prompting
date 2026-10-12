import json
import csv
import io

# List of allowed serialization methods (security‑controlled)
ALLOWED_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not recognized or disallowed.
    """
    method = format_method.lower()

    if method not in ALLOWED_METHODS:
        raise ValueError(f"Deserialization format '{format_method}' is not allowed.")

    # ---- JSON deserialization (safe) ---------------------------------
    if method == "json":
        try:
            # json.loads expects a string; decode bytes safely using UTF-8
            return json.loads(data_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data.") from exc

    # ---- CSV deserialization ------------------------------------------
    if method == "csv":
        try:
            text = data_bytes.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]
        except (UnicodeDecodeError, csv.Error) as exc:
            raise ValueError("Invalid CSV data.") from exc

    # The code should never reach here because of the ALLOWED_METHODS check
    raise ValueError(f"Unhandled deserialization method: {format_method}")