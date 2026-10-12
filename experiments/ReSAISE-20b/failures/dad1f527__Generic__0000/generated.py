import json
import pickle
from pathlib import Path


def load_serialized_data(filepath: str, data_format: str):
    """
    Load and deserialize data from a file using only whitelisted formats.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    data_format : str
        One of 'json', 'text', or 'pickle'. Any other value will raise a ValueError.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_format` is not in the allowed whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    # Whitelist of safe formats
    allowed_formats = {"json", "text", "pickle"}

    if data_format not in allowed_formats:
        raise ValueError(
            f"Untrusted or unsupported format '{data_format}'. "
            "Allowed formats are: json, text, pickle."
        )

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File '{filepath}' does not exist.")

    with path.open("rb") as f:
        raw_data = f.read()

    if data_format == "json":
        # Decode bytes to str for json.loads
        text_data = raw_data.decode("utf-8")
        return json.loads(text_data)

    if data_format == "text":
        # Return plain string
        return raw_data.decode("utf-8")

    if data_format == "pickle":
        # Pickle is inherently unsafe; use it only when explicitly requested.
        return pickle.loads(raw_data)