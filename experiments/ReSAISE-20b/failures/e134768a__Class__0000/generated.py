import json
from typing import Any


# A set of safe, explicitly allowed formats for deserialization.
SAFE_FORMATS = {"json"}


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from a trusted format.

    Parameters
    ----------
    byte_data : bytes
        Binary payload to deserialize.
    struct_format : str
        The format used for deserialization. Only formats listed in SAFE_FORMATS are allowed.

    Returns
    -------
    Any
        The Python object produced by deserialization.

    Raises
    ------
    ValueError
        If the requested format is not recognized or deemed unsafe.
    json.JSONDecodeError
        If the data cannot be decoded as JSON (when struct_format == 'json').
    """
    fmt = struct_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: '{struct_format}'")

    if fmt == "json":
        # JSON is safe as long as we don't allow arbitrary code execution.
        text = byte_data.decode("utf-8")
        return json.loads(text)

    # This point should never be reached because of the SAFE_FORMATS check,
    # but it keeps type-checkers happy.
    raise ValueError(f"Unhandled format: '{struct_format}'")