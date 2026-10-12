import json
import configparser
from typing import Any, Union


def load_serialized_content(
    serialized_input: bytes,
    serialization_format: str
) -> Union[Any, configparser.ConfigParser]:
    """
    Deserialize binary data safely.

    Parameters
    ----------
    serialized_input : bytes
        The raw input data.
    serialization_format : str
        Format used for deserialization. Supported values are:
            - 'json'  : standard JSON
            - 'ini'   : INI configuration format

    Returns
    -------
    Any | configparser.ConfigParser
        The deserialized Python object. For JSON it returns a native Python data
        structure; for INI it returns a ConfigParser instance.

    Raises
    ------
    ValueError
        If the format is not supported or deserialization fails.
    """
    # Normalize format string to lowercase
    fmt = serialization_format.strip().lower()

    if fmt == "json":
        try:
            text = serialized_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input is not valid UTF-8 for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON data") from exc

    if fmt == "ini":
        # configparser expects a string; we read it from the bytes
        try:
            text = serialized_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input is not valid UTF-8 for INI") from exc

        parser = configparser.ConfigParser()
        try:
            # read_string expects a file-like string
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError("Failed to parse INI data") from exc
        return parser

    # If we reach here, the format is unsupported
    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")