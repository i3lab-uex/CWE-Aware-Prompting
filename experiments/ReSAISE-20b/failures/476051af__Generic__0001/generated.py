import json
import configparser
from io import BytesIO

__all__ = ["deserialize_binary_data"]

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Safely deserialize binary data from a limited set of supported formats.

    Parameters
    ----------
    bin_data : bytes
        Binary representation of the serialized data.
    format_type : str
        The serialization format to use. Supported values are:
            - "json"   – JSON text encoded in UTF‑8.
            - "ini"    – INI configuration file format.

    Returns
    -------
    Any
        The Python object resulting from the deserialization process.

    Raises
    ------
    ValueError
        If ``format_type`` is not one of the supported, or if deserialization fails.
    """
    fmt = format_type.lower()

    # ------------------------------------------------------------------
    # JSON: use the standard library with UTF‑8 decoding.
    # ------------------------------------------------------------------
    if fmt == "json":
        try:
            text = bin_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON data: {exc}") from exc

    # ------------------------------------------------------------------
    # INI: use configparser; return a dictionary representation.
    # ------------------------------------------------------------------
    if fmt == "ini":
        try:
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object.
            parser.read_file(BytesIO(bin_data))
            result = {}
            for section in parser.sections():
                result[section] = dict(parser.items(section))
            return result
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError(f"Failed to parse INI data: {exc}") from exc

    # ------------------------------------------------------------------
    # Unsupported formats are explicitly rejected to avoid unsafe
    # deserialization (e.g., pickle, marshal, etc.).
    # ------------------------------------------------------------------
    raise ValueError(f"Unsupported or unsafe format: {format_type}")