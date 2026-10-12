import json
from configparser import ConfigParser, Error as ConfigError
from io import BytesIO

__all__ = ["deserialize_binary_data"]

# A whitelist of safe formats that may be deserialized
_SAFETY_WHITELIST = {"json", "ini"}


def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Deserialize binary data from a trusted source.

    Parameters
    ----------
    bin_data : bytes
        The serialized binary data.
    format_type : str
        The serialization format. Supported values are 'json' and 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is unsupported or considered unsafe.
    """
    if not isinstance(bin_data, (bytes, bytearray)):
        raise TypeError("bin_data must be a bytes-like object")

    fmt = format_type.lower()
    if fmt not in _SAFETY_WHITELIST:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}")

    if fmt == "json":
        # JSON is safe for deserialization of basic data types
        try:
            text = bin_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        # Use configparser to read INI data safely
        parser = ConfigParser()
        try:
            with BytesIO(bin_data) as fp:
                parser.read_file(fp)
        except (ConfigError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the parsed configuration into a plain dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result