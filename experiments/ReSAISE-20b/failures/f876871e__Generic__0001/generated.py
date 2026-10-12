import json
import pickle
from pathlib import Path

def deserialize_file_data(input_filepath: str, input_format: str):
    """
    Deserialize data from a file using only whitelisted formats.

    Parameters
    ----------
    input_filepath : str
        Path to the file containing the serialized data.
    input_format : str
        Format of the serialized data. Allowed values are:
            'json'   – JSON format.
            'text'   – Plain text; returns the string contents.
            'pickle' – Python pickle format (use with caution).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    allowed_formats = {"json", "text", "pickle"}

    if input_format not in allowed_formats:
        raise ValueError(
            f"Unsupported or unsafe format '{input_format}'. "
            f"Allowed formats: {', '.join(sorted(allowed_formats))}"
        )

    file_path = Path(input_filepath)

    if not file_path.is_file():
        raise FileNotFoundError(f"File '{input_filepath}' does not exist or is not a regular file.")

    if input_format == "json":
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if input_format == "text":
        with file_path.open("r", encoding="utf-8") as f:
            return f.read()

    # input_format == "pickle"
    # NOTE: Pickle is inherently unsafe.  Only use this when you
    # absolutely trust the source of the data.
    with file_path.open("rb") as f:
        return pickle.load(f)