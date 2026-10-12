import json
import pickle
from pathlib import Path

def deserialize_file_data(input_filepath: str, input_format: str):
    """
    Deserialize data from a file whose format is explicitly trusted.

    Parameters
    ----------
    input_filepath : str
        Path to the file containing serialized data.
    input_format : str
        Format of the serialized data. Must be one of the whitelisted options:
        'json', 'text' or 'pickle'.

    Returns
    -------
    object
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist or if a pickle file
        does not contain a valid protocol header (to mitigate accidental
        execution of malicious payloads).
    """
    # Whitelist of allowed formats
    _ALLOWED_FORMATS = {"json", "text", "pickle"}

    if input_format not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {input_format}")

    # Resolve the file path and ensure it exists
    file_path = Path(input_filepath)
    if not file_path.is_file():
        raise FileNotFoundError(f"File does not exist: {input_filepath}")

    # Use a context manager to guarantee the file is closed (CWE‑664 mitigation)
    with file_path.open("rb") as f:
        data_bytes = f.read()

    # Deserialize according to the requested format
    if input_format == "json":
        try:
            # Decode bytes to str before parsing JSON
            return json.loads(data_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if input_format == "text":
        try:
            return data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 text data") from exc

    if input_format == "pickle":
        # Quick sanity check: pickle protocol headers start with 0x80
        if not data_bytes.startswith(b"\x80"):
            raise ValueError("Pickle payload does not start with a valid protocol header")

        try:
            # Use pickle.loads with the highest safe protocol available
            return pickle.loads(data_bytes)
        except Exception as exc:
            raise ValueError("Failed to deserialize pickle data") from exc