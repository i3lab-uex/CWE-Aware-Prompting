import json
import configparser
from io import BytesIO

# List of safe, supported serialization formats
SAFE_FORMATS = {
    "json",
    "ini",   # key‑value configuration format
}

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Safely deserialize binary payloads that come from untrusted sources.

    Parameters
    ----------
    payload_bytes : bytes
        The binary representation of the serialized data.
    schema_type : str
        A string describing the serialization format. Only a curated set of
        safe formats is accepted ('json', 'ini').

    Returns
    -------
    object
        The deserialized Python object (e.g., dict, list, etc.).

    Raises
    ------
    ValueError
        If the requested format is unsupported or considered unsafe.
    json.JSONDecodeError, configparser.Error
        If the payload cannot be parsed with the chosen format.
    """
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be of type 'bytes'")

    if schema_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {schema_type!r}")

    if schema_type == "json":
        # JSON is safe when strict parsing is used
        return json.loads(payload_bytes.decode("utf-8"))

    if schema_type == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file‑like object
        with BytesIO(payload_bytes) as f:
            parser.read_file(f)
        # Convert the ConfigParser object to a plain dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # The code path should never reach here because of the SAFE_FORMATS check
    raise ValueError(f"Unhandled format: {schema_type!r}")