import json
import configparser
import io

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Safely deserialize binary payloads that come from external sources.

    Parameters
    ----------
    payload_bytes : bytes
        The binary representation of the serialized data.
    schema_type : str
        One of the supported format identifiers:
            - 'json'  : JSON encoded data.
            - 'ini'   : INI / configparser style data.

    Returns
    -------
    object
        The Python object resulting from deserialization.
        For JSON this will be a dict/list/etc.  For INI this
        is a plain dictionary mapping section names to option
        dictionaries.

    Raises
    ------
    ValueError
        If the requested schema_type is unsupported or deemed unsafe.
    """
    # Normalise the format identifier
    fmt = schema_type.strip().lower()

    if fmt == 'json':
        # JSON is safe to load from a string
        try:
            text = payload_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON payload: {exc}") from exc

    elif fmt == 'ini':
        # configparser can read from a file‑like object.
        parser = configparser.ConfigParser()
        # Use BytesIO to avoid leaving a file descriptor open.
        with io.BytesIO(payload_bytes) as f:
            try:
                parser.read_file(f)
            except configparser.Error as exc:
                raise ValueError(f"Invalid INI payload: {exc}") from exc

        # Convert the ConfigParser object to a plain dict for easier use.
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    else:
        # Explicitly disallow unsafe formats such as pickle, yaml, etc.
        raise ValueError(f"Unsupported or unsafe serialization format: {schema_type}")