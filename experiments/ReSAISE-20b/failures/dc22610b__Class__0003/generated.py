import json
import pickle
from pathlib import Path

def handle_serialized_file(serialized_file_path: str, serialization_format: str):
    """
    Deserialize data from a file using only whitelisted formats.

    Supported formats:
        - 'json'   : JSON data
        - 'text'   : Plain text (string)
        - 'pickle' : Pickle data (trusted only if explicitly allowed)

    Parameters
    ----------
    serialized_file_path : str
        Path to the file containing serialized data.
    serialization_format : str
        Format of the serialized data. Must be one of the supported formats.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist.
    FileNotFoundError
        If the file does not exist.
    Exception
        For any deserialization errors (JSONDecodeError, pickle.UnpicklingError, etc.).
    """
    # Whitelist of allowed formats
    _ALLOWED_FORMATS = {"json", "text", "pickle"}

    if serialization_format not in _ALLOWED_FORMATS:
        raise ValueError(
            f"Untrusted or unsupported serialization format '{serialization_format}'. "
            "Only 'json', 'text', and 'pickle' are allowed."
        )

    file_path = Path(serialized_file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File '{serialized_file_path}' does not exist or is not a file.")

    try:
        if serialization_format == "json":
            with file_path.open("r", encoding="utf-8") as f:
                return json.load(f)

        elif serialization_format == "text":
            with file_path.open("r", encoding="utf-8") as f:
                return f.read()

        elif serialization_format == "pickle":
            # Pickle is inherently unsafe; only use if explicitly trusted.
            with file_path.open("rb") as f:
                return pickle.load(f)

    except (json.JSONDecodeError, pickle.UnpicklingError) as e:
        # Wrap the underlying exception to provide context
        raise Exception(f"Deserialization failed for format '{serialization_format}': {e}") from e