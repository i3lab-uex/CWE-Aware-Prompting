import json
import configparser
from typing import Any, Dict


def convert_serialized_data(raw_bytes: bytes, format_hint: str) -> Any:
    """
    Deserialize binary data using a safe and curated set of formats.

    Supported formats (case‑insensitive):
        - 'json': JSON data
        - 'ini' or 'configparser': INI configuration

    Parameters
    ----------
    raw_bytes : bytes
        The serialized data in binary form.
    format_hint : str
        Hint indicating which deserialization routine to use.

    Returns
    -------
    Any
        The Python object resulting from the deserialization process.

    Raises
    ------
    ValueError
        If the format_hint is unsupported or if deserialization fails.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise ValueError("raw_bytes must be a bytes-like object")

    fmt = format_hint.strip().lower()
    try:
        if fmt == "json":
            # JSON is safe; decode bytes to str
            text = raw_bytes.decode("utf-8")
            return json.loads(text)

        if fmt in {"ini", "configparser"}:
            # configparser requires a file-like object; use StringIO
            import io

            text = raw_bytes.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_file(io.StringIO(text))
            # Convert to a plain dict for easier use
            config_dict: Dict[str, Dict[str, str]] = {
                section: dict(parser.items(section)) for section in parser.sections()
            }
            return config_dict

        # Explicitly reject unsafe formats such as pickle
        if fmt in {"pickle", "pkl"}:
            raise ValueError("pickle deserialization is disallowed for security reasons")

        # Any other format is unsupported
        raise ValueError(f"Unsupported format_hint: {format_hint!r}")

    except (json.JSONDecodeError, configparser.Error) as exc:
        # Wrap and re‑raise to provide a consistent error type
        raise ValueError(f"Failed to deserialize data as {format_hint!r}: {exc}") from exc