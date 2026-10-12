import json
from configparser import ConfigParser
from io import BytesIO


def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data safely based on a limited set of supported formats.

    Parameters
    ----------
    raw_bytes : bytes
        The serialized data in binary form.
    format_hint : str
        A hint indicating the serialization format. Supported values are:
            - 'json'  : JSON encoded data.
            - 'ini'   : INI configuration format.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_hint is unsupported or deemed unsafe (e.g., 'pickle').
    """
    fmt = format_hint.strip().lower()

    if fmt == "json":
        # JSON is safe for deserialization; ensure UTF‑8 decoding.
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc
        return json.loads(text)

    if fmt == "ini":
        # Parse INI data into a dictionary of dictionaries.
        parser = ConfigParser()
        try:
            # ConfigParser expects a file-like object; BytesIO gives us that.
            parser.read_file(BytesIO(raw_bytes))
        except Exception as exc:
            raise ValueError("Invalid INI data") from exc

        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Any other format is considered unsafe or unsupported.
    raise ValueError(f"Unsupported or unsafe serialization format: {format_hint}")