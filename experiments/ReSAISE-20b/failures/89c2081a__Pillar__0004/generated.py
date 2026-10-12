import json
from configparser import ConfigParser
from io import BytesIO
from typing import Any, Dict

# A whitelist of safe deserialization formats.
SAFE_FORMATS = {"json", "ini"}


def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Deserialize binary payloads using only safe and supported formats.

    Parameters
    ----------
    payload_bytes : bytes
        Binary data to deserialize.
    schema_type : str
        Format identifier: 'json' or 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported, unsafe, or deserialization fails.
    """
    if not isinstance(payload_bytes, (bytes, bytearray)):
        raise ValueError("payload_bytes must be a bytes-like object")

    schema_type = schema_type.lower()
    if schema_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {schema_type}")

    try:
        if schema_type == "json":
            # json.loads accepts str, bytes or bytearray.
            return json.loads(payload_bytes.decode("utf-8"))

        if schema_type == "ini":
            parser = ConfigParser()
            # Use BytesIO to avoid creating a temporary file.
            with BytesIO(payload_bytes) as stream:
                parser.read_file(stream)
            # Convert to a plain dict for easier consumption.
            config_dict: Dict[str, Dict[str, str]] = {}
            for section in parser.sections():
                config_dict[section] = dict(parser.items(section))
            return config_dict

    except Exception as exc:
        # Wrap any deserialization exception in ValueError to keep the API simple.
        raise ValueError(f"Deserialization failed for format '{schema_type}': {exc}") from exc