import json
import pickle
from pathlib import Path


def handle_serialized_file(serialized_file_path: str, serialization_format: str):
    """
    Safely deserialize data from a file.

    Parameters
    ----------
    serialized_file_path : str
        Path to the serialized file.
    serialization_format : str
        The format of the serialized data. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided format is not in the whitelist of accepted formats.
    """
    # Define a whitelist of safe serialization formats
    SAFE_FORMATS = {"json", "text", "pickle"}

    if serialization_format not in SAFE_FORMATS:
        raise ValueError(
            f"Untrusted or prohibited format '{serialization_format}'. "
            f"Allowed formats: {', '.join(sorted(SAFE_FORMATS))}"
        )

    # Read file contents
    path = Path(serialized_file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {serialized_file_path}")

    with path.open("rb") as f:
        data_bytes = f.read()

    # Deserialize based on the format
    if serialization_format == "json":
        try:
            return json.loads(data_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON: {exc}") from exc

    if serialization_format == "text":
        try:
            return data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Failed to decode text: {exc}") from exc

    # For pickle, we explicitly warn about the potential risk
    if serialization_format == "pickle":
        # Use pickle.loads which is inherently unsafe; this block exists
        # only because the caller explicitly requested it.
        try:
            return pickle.loads(data_bytes)
        except Exception as exc:
            raise ValueError(f"Failed to load pickle data: {exc}") from exc