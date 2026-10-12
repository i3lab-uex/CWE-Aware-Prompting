import json
import configparser
import io

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Safely deserialize binary data based on a given format hint.

    Parameters
    ----------
    raw_bytes : bytes
        Binary representation of the serialized data.
    format_hint : str
        One of 'json' or 'ini'. Other values raise an exception.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_hint is unsupported or if deserialization fails.
    """
    fmt = format_hint.lower()

    # Ensure the data is decoded as UTF-8 text
    try:
        text = raw_bytes.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode bytes as UTF-8: {exc}") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except Exception as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(io.StringIO(text))
        except Exception as exc:
            raise ValueError(f"INI deserialization error: {exc}") from exc

        # Convert the ConfigParser object to a plain dictionary
        config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
        return config_dict

    # Disallow any other format, including pickle
    raise ValueError(f"Unsupported or unsafe format: {format_hint!r}")