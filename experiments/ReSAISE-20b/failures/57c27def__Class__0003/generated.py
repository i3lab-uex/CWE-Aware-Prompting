import json
import configparser
from typing import Any, Dict


# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}


def convert_serialized_data(raw_bytes: bytes, format_hint: str) -> Any:
    """
    Deserialize binary data using a safe, pre‑approved format.

    Parameters
    ----------
    raw_bytes : bytes
        The serialized data in binary form.
    format_hint : str
        One of the safe formats ('json', 'ini') indicating how to deserialize.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_hint is not supported or if deserialization fails.
    """
    fmt = format_hint.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_hint}")

    try:
        if fmt == "json":
            # Decode bytes to string; enforce strict UTF‑8 decoding.
            text = raw_bytes.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            # configparser reads from a string; convert to dict.
            parser = configparser.ConfigParser()
            text = raw_bytes.decode("utf-8")
            parser.read_string(text)
            # Convert to a plain dictionary for easier use.
            return {section: dict(parser.items(section)) for section in parser.sections()}

    except Exception as exc:
        # Wrap any exception to provide a clear error message.
        raise ValueError(f"Failed to deserialize data as {format_hint}: {exc}") from exc