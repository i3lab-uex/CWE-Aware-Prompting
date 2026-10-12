import json
import configparser
from io import BytesIO
from typing import Any


def deserialize_binary_data(bin_data: bytes, format_type: str) -> Any:
    """
    Deserialize binary data that comes from an external source.

    Only a small, curated set of formats is supported.  All other
    formats raise an exception to avoid the dangers of arbitrary code
    execution (CWE‑502).

    Supported formats:

        * json   – JSON text encoded as UTF-8
        * ini    – INI configuration data

    Parameters
    ----------
    bin_data : bytes
        The binary payload containing the serialized representation.
    format_type : str
        One of ``'json'`` or ``'ini'``.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    ValueError
        If ``format_type`` is not supported or if the data cannot be parsed.
    """
    # Normalise format name
    fmt = format_type.strip().lower()

    if fmt == "json":
        try:
            text = bin_data.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("JSON payload must be valid UTF‑8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use BytesIO
            parser.read_file(BytesIO(bin_data))
        except Exception as exc:  # pragma: no cover
            raise ValueError("Invalid INI data") from exc

        # Convert to a plain dict of dicts
        return {section: dict(parser[section]) for section in parser.sections()}

    # Any other format is disallowed
    raise ValueError(f"Unsupported or unsafe deserialization format: {format_type}")