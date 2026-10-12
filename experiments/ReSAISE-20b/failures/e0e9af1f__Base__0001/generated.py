import json
import pickle
from pathlib import Path

# Whitelist of safe formats that the function is allowed to handle.
ALLOWED_FORMATS = {"json", "text", "pickle"}


def load_serialized_data(file_location: str, data_format: str):
    """
    Load and deserialize data from a file located at `file_location`.

    Parameters
    ----------
    file_location : str
        Path to the serialized data file.
    data_format : str
        The format of the serialized data. Must be one of the allowed formats:
        'json', 'text', or 'pickle'.

    Returns
    -------
    object
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the supplied format is not in the whitelist of allowed formats.
    FileNotFoundError
        If the specified file does not exist.
    """
    # Validate format against the whitelist
    if data_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}. "
                         f"Allowed formats are: {sorted(ALLOWED_FORMATS)}")

    path = Path(file_location)

    if not path.is_file():
        raise FileNotFoundError(f"No such file: {file_location!r}")

    # Handle each format explicitly
    if data_format == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if data_format == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    if data_format == "pickle":
        with path.open("rb") as f:
            return pickle.load(f)