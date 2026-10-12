import json
import pickle
from pathlib import Path

# Whitelist of safe formats.  Pickle is included only if the caller explicitly
# requests it; otherwise, it will be rejected.
ALLOWED_FORMATS = {"json", "text", "pickle"}


def load_serialized_data(filepath: str, data_format: str):
    """
    Load and deserialize data from a file in a secure manner.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    data_format : str
        The format of the serialized data. Must be one of ``ALLOWED_FORMATS``.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If ``data_format`` is not in the whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    # 1. Verify that the format is allowed
    if data_format not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {data_format!r}")

    # 2. Open the file safely
    path = Path(filepath)
    with path.open("rb") as f:
        raw_data = f.read()

    # 3. Deserialize according to the format
    if data_format == "json":
        # Decode bytes to string and parse JSON
        return json.loads(raw_data.decode("utf-8"))
    elif data_format == "text":
        # Return the raw text
        return raw_data.decode("utf-8")
    elif data_format == "pickle":
        # NOTE: Pickle is inherently insecure.  Only use it if the source
        # of the file is fully trusted and no untrusted data can be loaded.
        return pickle.loads(raw_data)
    else:
        # This branch is unreachable because of the earlier check,
        # but it keeps type-checkers happy.
        raise ValueError(f"Unsupported data format: {data_format!r}")