import json
import pickle
from pathlib import Path

# Whitelist of formats considered safe for this context.
ALLOWED_FORMATS = {"json", "text", "pickle"}

def deserialize_file_data(input_filepath: str, input_format: str):
    """
    Deserialize data from a file using only whitelisted formats.

    Parameters
    ----------
    input_filepath : str
        Path to the file containing serialized data.
    input_format : str
        Format of the serialized data. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    object
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If `input_format` is not in the whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    if input_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {input_format!r}")

    path = Path(input_filepath)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {input_filepath!r}")

    # Read the file content according to the format
    if input_format == "text":
        # Return the raw text string (decoded as UTF‑8)
        return path.read_text(encoding="utf-8")
    else:
        # For json and pickle we read binary data
        raw = path.read_bytes()

    if input_format == "json":
        # Decode JSON into Python objects
        return json.loads(raw.decode("utf-8"))
    elif input_format == "pickle":
        # NOTE: pickle is inherently unsafe if the source is untrusted.
        # The caller must ensure that only trusted data reaches this function.
        return pickle.loads(raw)

    # This point should never be reached due to the whitelist check
    raise ValueError(f"Unhandled format: {input_format!r}")