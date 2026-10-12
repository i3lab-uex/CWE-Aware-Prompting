import json
import pickle
from pathlib import Path
from typing import Any


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load a serialized object from *filepath* using only the
    whitelisted formats.  The function uses safe deserialization
    practices and rejects any untrusted or unsupported format.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    data_format : str
        Format of the serialized data. Must be one of:
        * 'json'   – JSON text
        * 'text'   – plain UTF‑8 text
        * 'pickle' – pickled Python object (use with caution)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *data_format* is not in the whitelist or if deserialization fails.
    """
    # Whitelist of allowed formats
    ALLOWED_FORMATS = {"json", "text", "pickle"}

    if data_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported serialization format: {data_format!r}")

    path = Path(filepath)

    try:
        if data_format == "json":
            with path.open("r", encoding="utf-8") as fp:
                return json.load(fp)

        if data_format == "text":
            with path.open("r", encoding="utf-8") as fp:
                return fp.read()

        # For pickle we explicitly read binary data.
        with path.open("rb") as fp:
            return pickle.loads(fp.read())

    except (OSError, json.JSONDecodeError, pickle.UnpicklingError) as exc:
        raise ValueError(f"Failed to load data from {filepath!r} using format '{data_format}'.") from exc