import json
import csv
import io

# List of trusted serialization formats
_TRUSTED_FORMATS = {"json", "csv"}


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str):
    """
    Recover a Python object from serialized byte data.

    Parameters
    ----------
    deserialized_bytes : bytes
        The raw byte stream containing the serialized data.
    method_for_serialization : str
        The serialization format used: 'json' or 'csv'.

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    fmt = method_for_serialization.lower()
    if fmt not in _TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or potentially unsafe serialization method: {method_for_serialization}"
        )

    # Convert bytes to string assuming UTF-8 encoding
    try:
        text = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded text") from exc

    if fmt == "json":
        # json.loads safely parses JSON into Python data structures
        return json.loads(text)

    if fmt == "csv":
        # csv module parses CSV into list of dictionaries
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # The code should never reach here due to the earlier check
    raise ValueError(f"Unhandled serialization format: {method_for_serialization}")