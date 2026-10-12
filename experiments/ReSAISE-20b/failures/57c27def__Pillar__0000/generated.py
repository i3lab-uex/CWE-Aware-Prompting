import json
import configparser
from typing import Any


class UnsupportedFormatError(RuntimeError):
    """Raised when the requested format is not supported or unsafe for deserialization."""


def convert_serialized_data(raw_bytes: bytes, format_hint: str) -> Any:
    """
    Deserialize binary data into a Python object based on a safe format hint.

    Parameters
    ----------
    raw_bytes : bytes
        The binary payload to be deserialized.
    format_hint : str
        One of the supported format identifiers: 'json', or 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    UnsupportedFormatError
        If the format_hint is not in the curated safe list or if deserialization fails.
    """
    # Ensure we have a string representation of the data
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UnsupportedFormatError(
            "Input data is not valid UTF‑8 encoded text."
        ) from exc

    fmt = format_hint.lower()
    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise UnsupportedFormatError("Invalid JSON payload.") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(text)
        except configparser.Error as exc:
            raise UnsupportedFormatError("Invalid INI payload.") from exc

        # Convert to a plain dict for easier consumption
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result

    # Any other format is considered unsafe or unsupported
    raise UnsupportedFormatError(f"Unsupported or unsafe deserialization format: {format_hint}")