import json
import configparser
from io import BytesIO


class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or unsafe format is requested."""
    pass


def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Safely deserializes binary data using only approved formats.

    Parameters
    ----------
    bin_data : bytes
        The serialized data in binary form.
    format_type : str
        The serialization format. Only 'json' and 'ini' are supported.

    Returns
    -------
    Any
        The deserialized Python object (dict for json/ini).

    Raises
    ------
    UnsupportedFormatError
        If the format is unsupported or unsafe.
    ValueError
        If the data cannot be parsed in the requested format.
    """
    fmt = format_type.lower()

    if fmt == "json":
        # json.loads accepts str, so decode assuming UTF‑8
        try:
            text = bin_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 data for JSON deserialization: {exc}") from exc
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file‑like object; use BytesIO
        try:
            with BytesIO(bin_data) as fp:
                parser.read_file(fp)
        except Exception as exc:  # configparser may raise ParsingError
            raise ValueError(f"Failed to parse INI data: {exc}") from exc

        # Convert to a nested dictionary
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result

    # Disallow unsafe formats like pickle, marshal, etc.
    raise UnsupportedFormatError(f"Deserialization format '{format_type}' is not supported or unsafe.")