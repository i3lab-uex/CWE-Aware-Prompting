import json
from pathlib import Path

# Whitelisted safe formats for deserialization
ALLOWED_FORMATS = {
    "json": json.load,
    "text": lambda f: f.read().strip(),
}

def load_serial_data(f_path: str, f_format: str):
    """
    Load and deserialize data from a file using only whitelisted formats.

    Parameters
    ----------
    f_path : str
        Path to the file containing the serialized data.
    f_format : str
        Format of the serialized data. Must be one of the allowed formats.

    Returns
    -------
    Any
        The deserialized Python object (for 'json' this will be a dict/list/etc.,
        for 'text' it will be the file contents as a string).

    Raises
    ------
    ValueError
        If f_format is not in the allowed whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    if f_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {f_format!r}")

    path = Path(f_path)
    with path.open("rb") as f:
        # Use the appropriate loader from the whitelist
        return ALLOWED_FORMATS[f_format](f)

# Example usage (commented out to avoid accidental execution):
# data = load_serial_data("data.json", "json")
# print(data)