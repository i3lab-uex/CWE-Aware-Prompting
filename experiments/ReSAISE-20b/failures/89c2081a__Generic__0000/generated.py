import json
import configparser
from io import StringIO
from typing import Any, Dict


def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Deserialize binary data safely according to the specified schema type.

    Parameters
    ----------
    payload_bytes : bytes
        The serialized data in binary form.
    schema_type : str
        The format to use for deserialization. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    ValueError
        If an unsupported or unsafe schema_type is supplied.
    """
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be a bytes object")

    if schema_type.lower() == "json":
        try:
            text = payload_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON payload: {exc}") from exc

    if schema_type.lower() == "ini":
        try:
            text = payload_bytes.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(text))
            # Convert the parsed data to a nested dictionary
            result: Dict[str, Dict[str, str]] = {
                section: dict(parser.items(section)) for section in parser.sections()
            }
            return result
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError(f"Failed to parse INI payload: {exc}") from exc

    # Any other format is considered unsupported/unsafe
    raise ValueError(f"Unsupported or unsafe schema_type: {schema_type!r}")