import json
import pickle
from pathlib import Path
from typing import Any

# Only these formats are considered safe
SAFE_FORMATS = {"json", "text", "pickle"}


def deserialize_file_data(filepath: str, serialization_format: str) -> Any:
    """
    Safely deserialize data from a file.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    serialization_format : str
        One of 'json', 'text' or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    if serialization_format not in SAFE_FORMATS:
        raise ValueError(f"Unsupported format: {serialization_format}")

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {filepath}")

    if serialization_format == "text":
        # Plain text – simply read as string
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    if serialization_format == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    # pickle
    with path.open("rb") as f:
        data = pickle.load(f)

    # Basic type check – only allow simple, non-executable objects
    allowed_types = (
        dict,
        list,
        tuple,
        set,
        str,
        int,
        float,
        bool,
        type(None),
    )
    if not isinstance(data, allowed_types):
        raise ValueError(
            f"Pickle payload contains unsafe type: {type(data).__name__}"
        )

    # Recursively ensure nested structures also contain only allowed types
    def _check(obj: Any):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _check(k)
                _check(v)
        elif isinstance(obj, (list, tuple, set)):
            for item in obj:
                _check(item)
        elif not isinstance(obj, allowed_types):
            raise ValueError(
                f"Pickle payload contains unsafe nested type: {type(obj).__name__}"
            )

    _check(data)
    return data