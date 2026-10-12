import json
from typing import Any

def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Safely deserialize `raw_data` according to the specified `method_name`.

    Supported formats:
        - 'json': Deserialized using json.loads with strict parsing.

    All other formats raise a ValueError to prevent unsafe deserialization.
    
    Parameters
    ----------
    raw_data : bytes
        The serialized object in byte format.
    method_name : str
        The name of the serialization method used ('json', 'xml', 'pickle', ...).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method_name is not supported or considered unsafe.
    """
    # Normalize method name to lower case for comparison
    method = method_name.strip().lower()

    if method == "json":
        try:
            # Decode bytes to string using UTF-8; raise if invalid
            json_str = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF-8 for JSON deserialization") from exc

        # json.loads can raise ValueError or JSONDecodeError
        try:
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    # If other formats are requested, refuse to process them
    raise ValueError(f"Unsupported or unsafe deserialization format: {method_name!r}")