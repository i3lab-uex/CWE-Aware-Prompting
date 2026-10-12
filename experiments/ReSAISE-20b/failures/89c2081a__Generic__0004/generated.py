import json
from configparser import ConfigParser
from io import BytesIO


def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Deserialize binary data according to a safe, curated format.

    Parameters
    ----------
    payload_bytes : bytes
        The binary data to deserialize.
    schema_type : str
        One of 'json', 'ini'.  Other values are rejected.

    Returns
    -------
    object
        The Python representation of the data.

    Raises
    ------
    ValueError
        If `schema_type` is unsupported or unsafe.
    """
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be a bytes object")

    schema_type = schema_type.lower()

    if schema_type == "json":
        try:
            return json.loads(payload_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if schema_type == "ini":
        parser = ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(BytesIO(payload_bytes))
        except Exception as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert to a nested dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported or unsafe schema_type: {schema_type}")