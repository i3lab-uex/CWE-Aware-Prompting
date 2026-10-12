import json
import pickle
from pathlib import Path


def handle_serialized_file(serialized_file_path: str, serialization_format: str):
    """
    Deserialize data from a file using only whitelisted formats.

    Parameters
    ----------
    serialized_file_path : str
        Path to the file containing the serialized data.
    serialization_format : str
        The format of the serialized data. Must be one of the whitelisted formats:
            - 'json'
            - 'text'
            - 'pickle'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the supplied format is not in the whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    # Define a whitelist of allowed formats. Pickle is included only for
    # completeness; it should be used with caution as it can execute arbitrary code.
    _WHITELIST = {"json", "text", "pickle"}

    if serialization_format not in _WHITELIST:
        raise ValueError(
            f"Untrusted or unsupported serialization format: {serialization_format}"
        )

    file_path = Path(serialized_file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {serialized_file_path}")

    # Open the file in binary mode for all formats; text format will be decoded later.
    with file_path.open("rb") as f:
        data_bytes = f.read()

    if serialization_format == "json":
        # JSON is safe; decode bytes to str and load.
        return json.loads(data_bytes.decode("utf-8"))

    if serialization_format == "text":
        # Return the raw string content.
        return data_bytes.decode("utf-8")

    if serialization_format == "pickle":
        # Pickle is inherently unsafe; only use it if the source is trusted.
        return pickle.loads(data_bytes)

    # This point should never be reached because of the whitelist check.
    raise ValueError(f"Unhandled serialization format: {serialization_format}")