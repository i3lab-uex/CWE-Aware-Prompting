import json
import configparser
from io import StringIO
from typing import Any


def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Safely deserialize binary data using only approved formats.

    Parameters
    ----------
    data_input : bytes
        The serialized data received in binary form.
    format_type : str
        The serialization mechanism used: 'json' or 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in the whitelist or if deserialization fails.
    """
    # Define a strict whitelist of allowed formats
    ALLOWED_FORMATS = {"json", "ini"}

    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Format '{format_type}' is not allowed or supported.")

    try:
        if fmt == "json":
            # json only handles text; decode bytes to str
            text = data_input.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            # ConfigParser expects a file-like object
            text = data_input.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(text))

            # Convert the parsed INI to a nested dictionary
            result = {}
            for section in parser.sections():
                result[section] = dict(parser.items(section))
            return result

    except Exception as exc:
        # Wrap any exception in a ValueError for consistency
        raise ValueError(f"Deserialization failed for format '{format_type}': {exc}") from exc