import json
from configparser import ConfigParser
from io import BytesIO

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json",
    "ini",   # INI files are parsed into a dictionary of sections.
}

def safely_deserialize_data(serialized_bytes: bytes, method_format: str):
    """
    Deserialize binary data using only permitted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw bytes containing the serialized data.
    method_format : str
        The serialization format used (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS or if deserialization fails.
    """
    fmt = method_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: '{method_format}'")

    try:
        if fmt == "json":
            # JSON is text-based; decode bytes to string first.
            return json.loads(serialized_bytes.decode("utf-8"))

        if fmt == "ini":
            # INI files are parsed into a dictionary of sections.
            parser = ConfigParser()
            parser.read_file(BytesIO(serialized_bytes))
            # Convert to a plain dict of dicts for easier use.
            return {section: dict(parser.items(section)) for section in parser.sections()}

    except Exception as exc:
        # Wrap any exception to provide a clear error message.
        raise ValueError(f"Deserialization failed for format '{method_format}': {exc}") from exc