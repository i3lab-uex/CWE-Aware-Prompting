import json
import configparser
from io import BytesIO

# List of safe formats we support
SAFE_FORMATS = {"json", "ini"}


def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Deserialize binary payloads safely.

    Parameters
    ----------
    payload_bytes : bytes
        The raw binary data to deserialize.
    schema_type : str
        The format of the payload. Supported values are 'json' and 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the schema_type is not in SAFE_FORMATS or if deserialization fails.
    """
    # Normalise the schema type
    fmt = schema_type.lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe schema type: {schema_type!r}")

    try:
        if fmt == "json":
            # JSON is safe for deserialization
            return json.loads(payload_bytes.decode("utf-8"))

        if fmt == "ini":
            # Parse INI into a nested dict
            parser = configparser.ConfigParser()
            parser.read_file(BytesIO(payload_bytes))
            # Convert to a plain dict
            result = {section: dict(parser[section]) for section in parser.sections()}
            return result

    except Exception as exc:
        # Wrap any exception to avoid leaking internal details
        raise ValueError(f"Failed to deserialize payload as {schema_type}") from exc