import json
import configparser
from typing import Any, Dict

def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from a trusted source using only safe formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data in binary form.
    struct_format : str
        The format used for deserialization. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is not recognized or deemed unsafe.
    """
    if not isinstance(byte_data, (bytes, bytearray)):
        raise TypeError("byte_data must be bytes or bytearray")

    fmt = struct_format.lower()
    try:
        if fmt == "json":
            # Decode UTF‑8 before parsing
            text = byte_data.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            # ConfigParser expects a file‑like object; use read_string
            parser = configparser.ConfigParser()
            # decode as UTF‑8
            text = byte_data.decode("utf-8")
            parser.read_string(text)
            # Convert to a plain dict of dicts
            return {section: dict(parser.items(section)) for section in parser.sections()}

        # If we reach here, the format is unsupported
        raise ValueError(f"Unsupported or unsafe deserialization format: {struct_format}")

    except (json.JSONDecodeError, configparser.Error) as exc:
        # Wrap parsing errors in a ValueError to avoid leaking implementation details
        raise ValueError(f"Failed to deserialize data with format '{struct_format}': {exc}") from exc