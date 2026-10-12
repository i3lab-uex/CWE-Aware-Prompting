import json
import configparser
from io import BytesIO


class UnsafeDeserializationError(RuntimeError):
    """Raised when an unsafe or unsupported serialization format is requested."""
    pass


def load_serialized_content(serialized_input: bytes, serialization_format: str):
    """
    Deserialize binary data from trusted formats only.

    Parameters
    ----------
    serialized_input : bytes
        The input binary data to deserialize.
    serialization_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    object
        The Python object represented by the input data.

    Raises
    ------
    UnsafeDeserializationError
        If the format is not supported or considered unsafe.
    ValueError
        If deserialization fails due to malformed input.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            # json.loads expects a str; decode using utf-8
            return json.loads(serialized_input.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        try:
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; BytesIO gives us one
            parser.read_file(BytesIO(serialized_input))
            # Convert the parsed sections to a nested dictionary
            config_dict = {
                section: dict(parser.items(section))
                for section in parser.sections()
            }
            return config_dict
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Invalid INI data") from exc

    # Any other format is considered unsafe or unsupported
    raise UnsafeDeserializationError(
        f"Unsupported or unsafe serialization format: {serialization_format}"
    )