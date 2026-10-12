import json
import configparser
from io import BytesIO

# Define the set of trusted formats.  Only these will be allowed.
TRUSTED_FORMATS = {
    "json",
    "ini",
}

def decode_serialized_data(data_bytes: bytes, format_string: str):
    """
    Safely deserialize data coming from an unreliable source.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data.
    format_string : str
        Identifier of the serialization format (e.g. 'json', 'ini').

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
        raise ValueError(f"Untrusted or unsupported format: {format_string!r}")

    # Perform deserialization according to the trusted format.
    if fmt == "json":
        try:
            return json.loads(data_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object with text data.
            parser.read_file(BytesIO(data_bytes))
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Failed to parse INI data") from exc

        # Convert the ConfigParser object into a nested dictionary.
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # The above guard should prevent reaching this point.
    raise ValueError(f"Unhandled trusted format: {format_string!r}")