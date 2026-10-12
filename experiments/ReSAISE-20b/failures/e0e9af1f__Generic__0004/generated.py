import json
import pickle
from pathlib import Path
from typing import Any


def load_serialized_data(file_location: str, data_format: str) -> Any:
    """
    Load and deserialize data from a file.

    Parameters
    ----------
    file_location : str
        Path to the serialized data file.
    data_format : str
        The format of the data. Must be one of the allowed formats:
        - 'json'  : JSON encoded data
        - 'text'  : Plain text (decoded as UTF‑8)
        - 'pickle': Pickle serialized data (use with caution)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not in the whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    # Whitelist of allowed formats
    ALLOWED_FORMATS = {"json", "text", "pickle"}

    if data_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format '{data_format}'. "
                         f"Allowed formats: {sorted(ALLOWED_FORMATS)}")

    file_path = Path(file_location)

    if not file_path.is_file():
        raise FileNotFoundError(f"File '{file_location}' does not exist.")

    # Read the file content
    if data_format == "text":
        with file_path.open("r", encoding="utf-8") as f:
            return f.read()
    else:  # 'json' or 'pickle'
        with file_path.open("rb") as f:
            data_bytes = f.read()

    if data_format == "json":
        # json.loads expects a str, so decode bytes
        return json.loads(data_bytes.decode("utf-8"))
    elif data_format == "pickle":
        # NOTE: pickle can execute arbitrary code. Use only with trusted sources.
        return pickle.loads(data_bytes)