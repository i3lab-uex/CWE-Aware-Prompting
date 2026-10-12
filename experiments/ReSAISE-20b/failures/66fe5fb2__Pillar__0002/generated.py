import json
import configparser
from io import BytesIO
from typing import Any


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize binary data safely using only permitted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary payload to be deserialized.
    method_format : str
        Identifier of the serialization format used.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or considered unsafe.
    """
    allowed_formats = {"json", "ini"}

    fmt = method_format.lower()
    if fmt not in allowed_formats:
        raise ValueError(f"Deserialization format '{method_format}' is not permitted.")

    if fmt == "json":
        try:
            return json.loads(serialized_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data.") from exc

    if fmt == "ini":
        config = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; BytesIO provides that.
            config.read_file(BytesIO(serialized_bytes))
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Failed to deserialize INI data.") from exc

        # Convert the ConfigParser object into a plain dictionary.
        return {section: dict(config[section]) for section in config.sections()}

    # This point should never be reached because of the allowed_formats check.
    raise ValueError(f"Unhandled format: {method_format}")