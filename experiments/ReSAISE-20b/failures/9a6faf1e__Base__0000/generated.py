import json
import pickle
from pathlib import Path
from typing import Any

# Whitelist of safe serialization formats
SAFE_FORMATS = {
    "json",
    "text",   # plain text, no deserialization needed
    "pickle", # only used when explicitly requested by the caller
}

def read_serialized_file(file_path: str, file_format: str) -> Any:
    """
    Safely deserialize the contents of a file whose format is specified by
    ``file_format``. Only formats listed in ``SAFE_FORMATS`` are accepted.

    Parameters
    ----------
    file_path : str
        Path to the serialized data file.
    file_format : str
        Serialization format. Must be one of ``SAFE_FORMATS``.

    Returns
    -------
    Any
        The deserialized Python object (or raw string for 'text').

    Raises
    ------
    ValueError
        If ``file_format`` is not in the whitelist or if the file cannot be read.
    """
    # Validate format
    if file_format not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {file_format}")

    path = Path(file_path)

    try:
        if file_format == "text":
            # Plain text – just read the raw string
            return path.read_text(encoding="utf-8")

        elif file_format == "json":
            # JSON – safe by design
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)

        elif file_format == "pickle":
            # Pickle is considered trusted only if explicitly requested.
            with path.open("rb") as f:
                return pickle.load(f)

    except (OSError, json.JSONDecodeError, pickle.UnpicklingError) as exc:
        # Wrap low‑level errors in a ValueError to keep the API simple.
        raise ValueError(f"Failed to deserialize {file_path!r} as {file_format}: {exc}") from exc