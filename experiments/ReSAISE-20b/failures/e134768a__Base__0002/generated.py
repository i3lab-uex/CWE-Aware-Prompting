import json
import configparser
from typing import Any, Dict

# Define the set of safe formats that are allowed for deserialization.
ALLOWED_FORMATS = {"json", "ini"}


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using only safe formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        The format identifier (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    ValueError
        If the format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = struct_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    try:
        if fmt == "json":
            # Decode bytes to string and parse JSON
            text = byte_data.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            # Parse INI into a nested dictionary
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; use BytesIO
            from io import BytesIO

            parser.read_file(BytesIO(byte_data))
            config_dict: Dict[str, Dict[str, str]] = {}
            for section in parser.sections():
                config_dict[section] = dict(parser.items(section))
            return config_dict

    except Exception as exc:
        # Wrap any exception in a ValueError to avoid leaking implementation details
        raise ValueError(f"Deserialization error for format {struct_format!r}: {exc}") from exc