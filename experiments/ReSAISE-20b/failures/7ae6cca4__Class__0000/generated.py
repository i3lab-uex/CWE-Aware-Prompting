import json
import configparser
from io import BytesIO

# Define the set of formats that are explicitly allowed.
ALLOWED_FORMATS = {"json", "ini"}

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
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    # Normalize the format string to lowercase for case‑insensitive matching
    fmt = format_string.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    try:
        if fmt == "json":
            # Ensure the data is UTF‑8 encoded text
            decoded_text = data_bytes.decode("utf-8")
            # json.loads is safe for trusted JSON; no code execution occurs
            return json.loads(decoded_text)

        if fmt == "ini":
            # configparser reads from a file‑like object
            parser = configparser.ConfigParser()
            with BytesIO(data_bytes) as fp:
                parser.read_file(fp)
            # Convert the ConfigParser object to a plain dictionary
            result = {section: dict(parser.items(section)) for section in parser.sections()}
            return result

    except Exception as exc:
        # Wrap any exception to avoid leaking low‑level details
        raise ValueError(f"Failed to deserialize data: {exc}") from None