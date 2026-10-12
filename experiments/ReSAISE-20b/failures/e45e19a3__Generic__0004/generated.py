import json
import xml.etree.ElementTree as ET
from typing import Any


def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize raw bytes into a Python object for trusted formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        Serialization format: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    # Supported formats
    allowed_formats = {"json", "xml"}

    if data_type not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe format: {data_type!r}")

    # Decode bytes to string assuming UTF‑8
    try:
        text = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8") from exc

    if data_type == "json":
        # json.loads is safe for standard JSON; no code execution
        return json.loads(text)

    if data_type == "xml":
        # Use ElementTree with entity resolution disabled
        parser = ET.XMLParser(resolve_entities=False)
        return ET.fromstring(text, parser=parser)

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {data_type!r}")