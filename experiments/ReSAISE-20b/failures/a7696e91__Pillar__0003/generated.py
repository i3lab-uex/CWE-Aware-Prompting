import json
import configparser
from typing import Any, Dict

class UnsupportedFormatError(ValueError):
    """Raised when an unsupported or unsafe serialization format is requested."""
    pass

def load_serialized_content(
    serialized_input: bytes,
    serialization_format: str
) -> Any:
    """
    Deserialize binary data from trusted formats only.

    Parameters
    ----------
    serialized_input : bytes
        The serialized data in binary form.
    serialization_format : str
        The format used for deserialization. Only 'json' and 'ini'
        are supported; all others raise an exception.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not in the allowed set.
    ValueError
        If the data cannot be parsed according to the format.
    """
    fmt = serialization_format.lower()
    try:
        if fmt == "json":
            # JSON is safe for deserialization
            text = serialized_input.decode("utf-8")
            return json.loads(text)

        elif fmt == "ini":
            # INI files are parsed into a ConfigParser instance.
            text = serialized_input.decode("utf-8")
            parser = configparser.ConfigParser()
            # read_string expects a string; use StringIO if needed.
            parser.read_string(text)
            # Convert to a nested dictionary for easier consumption
            result: Dict[str, Dict[str, str]] = {
                section: dict(parser.items(section))
                for section in parser.sections()
            }
            return result

        else:
            # Any other format is considered unsafe or unsupported
            raise UnsupportedFormatError(
                f"Unsupported serialization format: '{serialization_format}'. "
                "Allowed formats are 'json' and 'ini'."
            )

    except Exception as exc:
        # Re‑raise with a more informative message
        raise ValueError(
            f"Failed to deserialize data as '{serialization_format}': {exc}"
        ) from exc