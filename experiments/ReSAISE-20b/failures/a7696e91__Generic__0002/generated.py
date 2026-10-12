import json
import configparser
from typing import Any, Dict


def load_serialized_content(
    serialized_input: bytes,
    serialization_format: str
) -> Any:
    """
    Deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    serialized_input : bytes
        The binary payload to deserialize.
    serialization_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object represented by the input data.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            # JSON expects text; decode using UTF‑8
            return json.loads(serialized_input.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects text; decode using UTF‑8
            parser.read_string(serialized_input.decode("utf-8"))
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert to a plain dictionary: {section: {key: value}}
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # If we reach here, the format is not supported
    raise ValueError(
        f"Unsupported or unsafe serialization format: {serialization_format}"
    )