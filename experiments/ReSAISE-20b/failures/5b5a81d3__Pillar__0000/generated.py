import json
import configparser
from io import BytesIO, StringIO
from typing import Any

# Define the set of safe formats that are allowed for deserialization.
SAFE_FORMATS = {"json", "ini"}

def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary payloads from trusted formats only.

    Parameters
    ----------
    byte_sequence : bytes
        Serialized data in binary form.
    data_format : str
        The format used for deserialization. Only values in SAFE_FORMATS are allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the data_format is not supported or if deserialization fails.
    """
    fmt = data_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    try:
        if fmt == "json":
            # JSON is text based; decode bytes to str using UTF-8.
            decoded = byte_sequence.decode("utf-8")
            return json.loads(decoded)

        if fmt == "ini":
            # INI files are also text; use ConfigParser to parse.
            with BytesIO(byte_sequence) as bio:
                parser = configparser.ConfigParser()
                # ConfigParser expects a file-like object that returns str,
                # so wrap BytesIO with TextIOWrapper.
                with StringIO(bio.read().decode("utf-8")) as sio:
                    parser.read_file(sio)
                # Convert ConfigParser object to a plain dict for easier consumption.
                result = {section: dict(parser[section]) for section in parser.sections()}
                return result

    except (UnicodeDecodeError, json.JSONDecodeError, configparser.Error) as exc:
        raise ValueError(f"Failed to deserialize payload: {exc}") from exc