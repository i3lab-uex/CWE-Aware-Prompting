import json
import configparser
from io import BytesIO

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Deserialize binary data from a safe set of formats.

    Parameters
    ----------
    bin_data : bytes
        The serialized data in binary form.
    format_type : str
        The format to use for deserialization. Supported values are:
        - 'json': JSON data (UTF‑8 encoded).
        - 'ini' : INI configuration data (UTF‑8 encoded).

    Returns
    -------
    object
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_type is unsupported or considered unsafe.
    """
    fmt = format_type.lower()

    if fmt == "json":
        # JSON is considered safe for deserialization.
        try:
            text = bin_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        # INI files are safe as they only contain configuration data.
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object.
            parser.read_file(BytesIO(bin_data))
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc
        # Convert the parser to a nested dictionary for easier use.
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # Disallow pickle and any other formats that could lead to arbitrary code execution.
    raise ValueError(f"Unsupported or unsafe format: {format_type}")