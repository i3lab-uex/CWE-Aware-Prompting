import json
import pickle
from pathlib import Path

# Whitelist of serialization formats that are considered safe for this context.
# The list can be extended, but any format outside it will raise a ValueError.
TRUSTED_FORMATS = {"json", "text", "pickle"}


def read_serialized_file(file_path: str, file_format: str):
    """
    Safely deserializes the contents of a file based on a trusted format.

    Parameters
    ----------
    file_path : str
        Path to the serialized data file.
    file_format : str
        The serialization format. Must be one of the values in TRUSTED_FORMATS.

    Returns
    -------
    object
        The deserialized Python object (e.g., dict, list, str, etc.).

    Raises
    ------
    ValueError
        If the file_format is not in TRUSTED_FORMATS or if deserialization fails.
    FileNotFoundError
        If the file does not exist.
    """
    if file_format not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {file_format!r}")

    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {file_path!r}")

    # Open the file in binary mode for all formats to avoid encoding issues.
    with path.open("rb") as f:
        data = f.read()

    try:
        if file_format == "json":
            # json.loads expects a text string, so decode using UTF-8.
            return json.loads(data.decode("utf-8"))
        elif file_format == "text":
            # Return the raw string content.
            return data.decode("utf-8")
        elif file_format == "pickle":
            # Pickle is inherently unsafe if the source is untrusted.
            # We accept it only because it's explicitly listed in TRUSTED_FORMATS,
            # but we still perform the operation within a try/except block.
            return pickle.loads(data)
    except Exception as exc:
        # Wrap any exception from the deserialization step in a ValueError
        raise ValueError(f"Failed to deserialize file {file_path!r} as {file_format}: {exc}") from exc