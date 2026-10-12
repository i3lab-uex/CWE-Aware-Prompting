import json
import configparser
from io import BytesIO
from typing import Any


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize binary data safely using only a whitelist of formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary payload to deserialize.
    method_format : str
        The serialization format used. Supported values are:
            - 'json'   -> JSON data.
            - 'ini'    -> INI configuration data.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    method_format = method_format.lower()

    if method_format == "json":
        try:
            text = serialized_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if method_format == "ini":
        try:
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; BytesIO provides that
            parser.read_file(BytesIO(serialized_bytes))
            # Convert to a plain dict for easier consumption
            return {section: dict(parser.items(section)) for section in parser.sections()}
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Failed to deserialize INI data") from exc

    # If we reach here, the format is unsupported
    raise ValueError(f"Deserialization for format '{method_format}' is not allowed.")