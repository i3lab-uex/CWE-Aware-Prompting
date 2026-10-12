import json
from configparser import ConfigParser
from io import BytesIO

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Safely deserialize binary data from a known set of formats.

    Parameters
    ----------
    payload_bytes : bytes
        The binary data to deserialize.
    schema_type : str
        One of 'json' or 'ini'. Any other value will raise an exception.

    Returns
    -------
    object
        The Python object resulting from deserialization.
        For JSON, this is the decoded value.
        For INI, this is a dictionary mapping section names to option dictionaries.

    Raises
    ------
    ValueError
        If `schema_type` is not supported or considered unsafe.
    """
    schema_type = schema_type.lower()

    if schema_type == "json":
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON payload is not valid UTF‑8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON payload") from exc

    if schema_type == "ini":
        parser = ConfigParser()
        try:
            # BytesIO allows ConfigParser to read bytes directly
            parser.read_file(BytesIO(payload_bytes))
        except Exception as exc:
            raise ValueError("Invalid INI payload") from exc
        # Convert to a plain dictionary for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # Explicitly disallow unsafe formats like pickle
    raise ValueError(f"Unsupported or unsafe schema type: {schema_type}")