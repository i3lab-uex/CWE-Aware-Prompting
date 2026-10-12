import json
import configparser
from io import BytesIO
from typing import Any

# Define the list of trusted formats that are allowed to be deserialized.
TRUSTED_FORMATS = {
    "json",
    "ini",
}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data based on a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format. Must be one of
        TRUSTED_FORMATS.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not in TRUSTED_FORMATS or if deserialization fails.
    """
    fmt = format_string.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    try:
        if fmt == "json":
            # JSON is text based; decode bytes to str safely.
            return json.loads(data_bytes.decode("utf-8"))
        elif fmt == "ini":
            # Use a BytesIO object as a file-like resource.
            parser = configparser.ConfigParser()
            with BytesIO(data_bytes) as f:
                # configparser expects a file-like object opened in text mode,
                # but BytesIO provides bytes; decode on the fly.
                parser.read_file(f, source="data_bytes")
            # Convert to a nested dict for easier use.
            return {section: dict(parser[section]) for section in parser.sections()}
    except Exception as exc:
        # Wrap any exception to avoid leaking internal details.
        raise ValueError(f"Failed to deserialize data for format {format_string!r}") from exc