import json
import csv
from io import StringIO
from typing import Any


# A whitelist of serialization methods that are considered safe.
_TRUSTED_METHODS = {"json", "csv"}


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Restore a Python object from a serialized byte stream.

    Parameters
    ----------
    deserialized_bytes : bytes
        The raw data to be deserialized.
    method_for_serialization : str
        Name of the serialization format used. Must be one of the trusted methods.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the serialization method is not trusted or if deserialization fails.
    """
    method = method_for_serialization.lower()

    if method not in _TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or potentially harmful serialization method: '{method}'. "
            f"Only the following methods are allowed: {sorted(_TRUSTED_METHODS)}"
        )

    try:
        if method == "json":
            # json.loads expects a string; decode UTF‑8 bytes safely.
            text = deserialized_bytes.decode("utf-8")
            return json.loads(text)

        if method == "csv":
            # CSV is read as text; decode UTF‑8 bytes safely.
            text = deserialized_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception to avoid leaking sensitive info.
        raise ValueError(f"Deserialization failed for method '{method}': {exc}") from exc