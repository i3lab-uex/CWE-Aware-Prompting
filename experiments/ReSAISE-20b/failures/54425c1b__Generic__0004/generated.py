import json
import configparser
from io import BytesIO


def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Safely deserialize binary data from a controlled set of formats.

    Parameters
    ----------
    data_input : bytes
        The serialized data received in binary form.
    format_type : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    object
        The deserialized Python object (e.g., dict, list).

    Raises
    ------
    ValueError
        If the format_type is not supported or explicitly disallowed.
    """
    # Normalise format type
    fmt = format_type.strip().lower()

    if fmt == "json":
        try:
            text = data_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF‑8 encoded") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "ini":
        # ConfigParser reads text, not bytes
        parser = configparser.ConfigParser()
        try:
            with BytesIO(data_input) as f:
                parser.read_file(f)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert to a plain dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    else:
        # All other formats are disallowed
        raise ValueError(f"Deserialization format '{format_type}' is not allowed.")