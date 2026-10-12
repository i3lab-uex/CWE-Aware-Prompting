import json
from configparser import ConfigParser, Error as ConfigError
from io import BytesIO
from typing import Any

# Define a set of safe formats that are allowed for deserialization.
SAFE_FORMATS = {"json", "ini"}


class UnsafeFormatError(ValueError):
    """Raised when an unsupported or unsafe format is requested."""
    pass


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary payloads only from a whitelist of safe formats.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized data in binary form.
    data_format : str
        The format of the payload. Supported values are 'json' and 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    UnsafeFormatError
        If the requested format is not in the whitelist.
    ValueError
        If the payload cannot be parsed for the requested format.
    """
    fmt = data_format.lower()
    if fmt not in SAFE_FORMATS:
        raise UnsafeFormatError(
            f"Deserialization for format '{data_format}' is not allowed."
        )

    if fmt == "json":
        # Ensure bytes are decoded as UTF-8 before parsing.
        try:
            text = byte_sequence.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON payload is not valid UTF-8.") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON payload.") from exc

    if fmt == "ini":
        parser = ConfigParser()
        try:
            # ConfigParser expects a file-like object.
            with BytesIO(byte_sequence) as fp:
                parser.read_file(fp)
        except (ConfigError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid INI payload.") from exc

        # Convert the ConfigParser object to a nested dictionary.
        config_dict = {
            section: dict(parser.items(section)) for section in parser.sections()
        }
        return config_dict