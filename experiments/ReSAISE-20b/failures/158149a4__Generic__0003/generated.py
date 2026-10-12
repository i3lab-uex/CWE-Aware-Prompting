import json
import pickle
from pathlib import Path
from typing import Any

# Define the list of trusted formats
TRUSTED_FORMATS = {"json", "text", "pickle"}

def load_serialized_data(filepath: str, format_type: str) -> Any:
    """
    Safely deserialize data from a file.

    Parameters
    ----------
    filepath : str
        Path to the file to be deserialized.
    format_type : str
        Serialization format. Must be one of TRUSTED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_type` is not in TRUSTED_FORMATS.
    FileNotFoundError
        If the file does not exist.
    """
    if format_type not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}. "
                         f"Allowed formats are: {sorted(TRUSTED_FORMATS)}")

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {filepath!r}")

    if format_type == "json":
        with path.open("rt", encoding="utf-8") as f:
            return json.load(f)

    if format_type == "text":
        with path.open("rt", encoding="utf-8") as f:
            return f.read()

    # For pickle we enforce a minimum protocol and use a safe Unpickler
    if format_type == "pickle":
        with path.open("rb") as f:
            # Restrict to protocol 4+ for security
            data = f.read()
            if len(data) < 2 or data[0] != 0x80:   # pickle header byte
                raise ValueError("Not a valid pickle file.")
            protocol = data[1]
            if protocol < 4:
                raise ValueError(f"Unsupported pickle protocol {protocol}. "
                                 "Only protocols >= 4 are allowed.")
            return pickle.loads(data, fix_imports=True)

    # This point should never be reached due to earlier check
    raise ValueError(f"Unhandled format: {format_type!r}")