import json
import configparser
from io import BytesIO

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Safely deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    bin_data : bytes
        Serialized data in binary form.
    format_type : str
        The format to use for deserialization. Accepted values are:
        - 'json': JSON text encoded as UTF‑8.
        - 'ini' : INI configuration data.

    Returns
    -------
    object
        The Python representation of the deserialized data.

    Raises
    ------
    ValueError
        If `format_type` is unsupported or unsafe (e.g., 'pickle').
    TypeError
        If `bin_data` is not of type bytes.
    """
    if not isinstance(bin_data, bytes):
        raise TypeError("bin_data must be of type 'bytes'")

    fmt = format_type.lower()

    if fmt == "json":
        # Decode as UTF‑8 and load with the standard json module.
        try:
            text = bin_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        return json.loads(text)

    if fmt == "ini":
        # ConfigParser reads from a file‑like object; use BytesIO.
        parser = configparser.ConfigParser()
        try:
            parser.read_file(BytesIO(bin_data))
        except Exception as exc:
            raise ValueError("Invalid INI data") from exc
        # Convert to a plain dict for easier consumption.
        return {section: dict(parser[section]) for section in parser.sections()}

    # Explicitly forbid potentially unsafe formats.
    if fmt == "pickle":
        raise ValueError("The 'pickle' format is unsafe and not supported.")

    # Any other format is considered unsupported.
    raise ValueError(f"Unsupported deserialization format: {format_type}")