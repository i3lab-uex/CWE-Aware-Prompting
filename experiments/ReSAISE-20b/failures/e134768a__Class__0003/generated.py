import json
import configparser
from io import BytesIO
from typing import Any, Dict


# A set of formats that are explicitly allowed for deserialization.
SAFE_FORMATS = {"json", "ini"}


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data safely from an untrusted source.

    Parameters
    ----------
    byte_data : bytes
        The serialized data in binary form.
    struct_format : str
        Identifier of the serialization format. Supported values are
        "json" and "ini".

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or considered unsafe.
    """
    if struct_format.lower() not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format}")

    if struct_format.lower() == "json":
        # JSON is safe as long as we only parse data, not execute it.
        return json.loads(byte_data.decode("utf-8"))

    # struct_format == "ini"
    parser = configparser.ConfigParser()
    try:
        parser.read_file(BytesIO(byte_data))
    except (configparser.Error, UnicodeDecodeError) as exc:
        raise ValueError("Invalid INI data") from exc

    # Convert the ConfigParser object into a plain dictionary for easier use.
    ini_dict: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        ini_dict[section] = dict(parser.items(section))
    return ini_dict