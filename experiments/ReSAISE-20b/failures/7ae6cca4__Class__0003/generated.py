import json
import configparser
from io import BytesIO

# Define the set of trusted formats.
TRUSTED_FORMATS = {"json", "ini"}

def decode_serialized_data(data_bytes: bytes, format_string: str):
    """
    Safely deserialize data from a trusted source.

    Parameters
    ----------
    data_bytes : bytes
        The binary payload to deserialize.
    format_string : str
        Identifier of the serialization format (e.g., 'json', 'ini').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or untrusted.
    """
    fmt = format_string.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    if fmt == "json":
        # Decode bytes to string safely using UTF-8 with strict error handling.
        text = data_bytes.decode("utf-8", errors="strict")
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; BytesIO provides that.
        with BytesIO(data_bytes) as f:
            parser.read_file(f)
        # Convert to a plain dict for easier consumption.
        return {section: dict(parser[section]) for section in parser.sections()}

    # The logic should never reach here because of the initial guard.
    raise ValueError(f"Unhandled format: {format_string!r}")