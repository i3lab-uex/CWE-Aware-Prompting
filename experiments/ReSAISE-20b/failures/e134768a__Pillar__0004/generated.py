import json
import configparser
from typing import Any


# Define a set of safe, non‑malicious formats for deserialization
SAFE_FORMATS = {"json", "ini"}


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using only predefined safe formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        The format used for deserialization. Allowed values are 'json' and 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not recognized or considered unsafe.
    """
    if struct_format.lower() not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    try:
        if struct_format.lower() == "json":
            # JSON is safe for arbitrary data; decode bytes to str
            text = byte_data.decode("utf-8")
            return json.loads(text)

        elif struct_format.lower() == "ini":
            # ConfigParser can parse INI files safely
            parser = configparser.ConfigParser()
            text = byte_data.decode("utf-8")
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(text)
            return parser

    except (json.JSONDecodeError, configparser.Error, UnicodeDecodeError) as exc:
        # Wrap low‑level errors in a generic ValueError to avoid leaking implementation details
        raise ValueError(f"Failed to deserialize data as {struct_format!r}: {exc}") from exc