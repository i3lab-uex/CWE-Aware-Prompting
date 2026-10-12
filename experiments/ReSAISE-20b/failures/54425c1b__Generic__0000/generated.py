import json
import configparser
from io import StringIO

__all__ = ["deserialize_data_safely"]

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json", "ini"}


def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Safely deserialize binary data according to the specified format.

    Parameters
    ----------
    data_input : bytes
        Serialized binary data received from an external source.
    format_type : str
        The serialization mechanism used. Supported values are:
            - 'json'  : JSON format.
            - 'ini'   : INI configuration file format.

    Returns
    -------
    object
        The Python representation of the deserialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of supported formats.
    UnicodeDecodeError
        If the binary data cannot be decoded as UTF‑8.
    json.JSONDecodeError
        For malformed JSON input.
    configparser.Error
        For malformed INI data.

    Notes
    -----
    Only formats listed in :data:`SAFE_FORMATS` are allowed to prevent
    arbitrary code execution or other security issues that can arise with
    formats such as pickle.
    """
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}")

    # Decode bytes to a string; strict decoding ensures errors are raised.
    try:
        text = data_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            "utf-8",
            data_input,
            exc.start,
            exc.end,
            f"Unable to decode bytes as UTF‑8: {exc}"
        ) from exc

    if format_type == "json":
        # json.loads safely parses JSON into Python objects
        return json.loads(text)

    if format_type == "ini":
        # Parse INI data into a ConfigParser object.
        parser = configparser.ConfigParser()
        # Using StringIO to feed the text into ConfigParser
        parser.read_file(StringIO(text))
        # Convert to a plain dictionary for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # This point is unreachable due to the earlier check, but kept for completeness.
    raise ValueError(f"Unhandled format: {format_type!r}")