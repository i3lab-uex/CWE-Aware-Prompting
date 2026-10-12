import json
import configparser
from io import BytesIO
from typing import Any


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data using a safe, predefined format.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        One of the supported formats: 'json' or 'ini'.

    Returns
    -------
    Any
        The Python object represented by the data.

    Raises
    ------
    ValueError
        If the requested format is not supported or if deserialization fails.
    """
    # Normalize format string
    fmt = struct_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes as UTF-8 text
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    elif fmt == "ini":
        try:
            parser = configparser.ConfigParser()
            # Use a BytesIO context manager to ensure the stream is closed
            with BytesIO(byte_data) as fp:
                parser.read_file(fp)
            # Convert the ConfigParser object into a plain dictionary
            return {section: dict(parser[section]) for section in parser.sections()}
        except Exception as exc:
            raise ValueError(f"Invalid INI data: {exc}") from exc

    else:
        # Explicitly reject all other formats
        raise ValueError(f"Unsupported or unsafe format: {struct_format}")