import json
from pathlib import Path

# Define a whitelist of *trusted* serialization formats.
# Only JSON and plain text are considered safe for untrusted data.
ALLOWED_FORMATS = {
    "json": json.load,
    # Text files are returned as a string; no deserialization needed.
    "text": lambda f: f.read(),
}

def load_serial_data(f_path: str, f_format: str):
    """
    Load and deserialize data from a file whose format is explicitly
    whitelisted. Untrusted or unsafe formats are rejected.

    Parameters:
        f_path (str): Path to the file containing serialized data.
        f_format (str): The format of the serialized data. Must be one
                        of the keys in ALLOWED_FORMATS.

    Returns:
        The deserialized Python object (e.g., dict for JSON, str for text).

    Raises:
        ValueError: If the requested format is not in ALLOWED_FORMATS.
        FileNotFoundError: If the file does not exist or cannot be opened.
    """
    # Ensure we only accept formats from our whitelist
    if f_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format '{f_format}'. "
                         f"Allowed formats: {', '.join(ALLOWED_FORMATS.keys())}")

    # Resolve the file path and open it in binary mode for JSON
    path = Path(f_path)
    with path.open("rb") as fh:
        # For JSON we need a text file; json.load can handle binary
        if f_format == "json":
            return ALLOWED_FORMATS[f_format](fh)
        # For plain text we read as UTF‑8
        elif f_format == "text":
            return ALLOWED_FORMATS[f_format](fh)