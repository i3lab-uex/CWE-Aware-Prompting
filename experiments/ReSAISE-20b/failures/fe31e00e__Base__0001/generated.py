import json
import configparser
from io import BytesIO
from typing import Any

# A list of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}

def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize binary data that was serialized using a permitted format.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary form.
    serialization_format : str
        The format used for serialization. Supported formats are defined in
        `ALLOWED_FORMATS`. Case-insensitive.

    Returns
    -------
    Any
        The Python object resulting from the deserialization process.

    Raises
    ------
    ValueError
        If the requested format is not in `ALLOWED_FORMATS`.
    json.JSONDecodeError, configparser.Error
        If the data cannot be parsed according to its format.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed serialization format: {serialization_format}")

    # Ensure that the input is bytes; if not, raise an error
    if not isinstance(byte_data, (bytes, bytearray)):
        raise TypeError("byte_data must be of type 'bytes' or 'bytearray'")

    if fmt == "json":
        # JSON is text-based; decode using UTF-8 (strict)
        text = byte_data.decode("utf-8", errors="strict")
        return json.loads(text)

    if fmt == "ini":
        # ConfigParser expects a file-like object; use BytesIO
        parser = configparser.ConfigParser()
        with BytesIO(byte_data) as fp:
            # ConfigParser expects UTF-8 by default
            parser.read_file(fp)
        # Convert the parsed data into a plain dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point should never be reached due to the earlier check
    raise RuntimeError("Unreachable code path in securely_load_data")