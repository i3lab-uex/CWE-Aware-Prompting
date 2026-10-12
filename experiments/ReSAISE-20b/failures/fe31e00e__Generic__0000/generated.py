import json
import configparser
from io import BytesIO
from typing import Any


def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary format.
    serialization_format : str
        Format used to serialize the data. Supported values are:
        - 'json'   : JSON format
        - 'ini'    : INI configuration file format

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided format is not in the allowed list.
    json.JSONDecodeError, configparser.Error
        Propagated if parsing fails for the respective format.
    """
    allowed_formats = {"json", "ini"}

    fmt = serialization_format.lower()
    if fmt not in allowed_formats:
        raise ValueError(
            f"Unsupported or disallowed serialization format: '{serialization_format}'. "
            f"Allowed formats are: {', '.join(sorted(allowed_formats))}."
        )

    if fmt == "json":
        # Decode bytes to string and parse JSON
        text = byte_data.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        # INI files are parsed into a ConfigParser instance.
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use BytesIO after decoding.
        with BytesIO(byte_data) as f:
            parser.read_file(f, encoding="utf-8")
        # Convert ConfigParser to a plain dict for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # The code should never reach here because of the earlier check,
    # but this return is kept for completeness.
    raise RuntimeError("Unreachable code path reached in securely_load_data.")