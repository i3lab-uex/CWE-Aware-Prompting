import json
import configparser
from typing import Any, Dict


# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}


def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Deserialize binary data using a safe and controlled set of formats.

    Parameters
    ----------
    data_input : bytes
        The serialized data received in binary format.
    format_type : str
        The serialization mechanism used (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not in the list of allowed formats.
    json.JSONDecodeError
        If JSON deserialization fails.
    configparser.Error
        If INI deserialization fails.
    """
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {format_type!r}")

    # Convert the binary input to a string using UTF-8 (common for text-based formats).
    try:
        decoded = data_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data input is not valid UTF-8 text") from exc

    if format_type == "json":
        # JSON is safe because it only constructs basic data types.
        return json.loads(decoded)

    if format_type == "ini":
        # INI files are parsed into a ConfigParser instance and then
        # converted to a plain dictionary for easier consumption.
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; we use read_string.
            parser.read_string(decoded)
        except configparser.Error as exc:
            raise configparser.Error("Failed to parse INI data") from exc

        # Convert ConfigParser object into a nested dictionary.
        ini_dict: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            ini_dict[section] = dict(parser.items(section))
        return ini_dict