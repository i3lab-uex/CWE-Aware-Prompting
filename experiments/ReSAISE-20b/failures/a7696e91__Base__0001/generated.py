import json
import configparser
from io import BytesIO
from typing import Any, Dict

# A whitelist of safe serialization formats.
ALLOWED_FORMATS = {"json", "ini"}

def load_serialized_content(serialized_input: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data that comes from an untrusted source.
    
    Only formats listed in ALLOWED_FORMATS are supported. Any other format
    will raise a ValueError.
    
    Parameters
    ----------
    serialized_input : bytes
        The binary data to deserialize.
    serialization_format : str
        One of the supported formats ('json', 'ini').

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    # Normalize and validate format
    fmt = serialization_format.strip().lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    if fmt == "json":
        try:
            text = serialized_input.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a text stream, so wrap bytes in BytesIO and decode.
            with BytesIO(serialized_input) as bio:
                parser.read_file(bio, source="input")
        except configparser.Error as exc:
            raise ValueError("Failed to parse INI data") from exc

        # Convert ConfigParser object to a plain dictionary.
        result: Dict[str, Dict[str, str]] = {
            section: dict(parser[section]) for section in parser.sections()
        }
        return result

    # This point should never be reached due to the whitelist check above.
    raise ValueError(f"Unhandled serialization format: {serialization_format!r}")