import json
from typing import Any

# List of trusted serialization formats.  Only these are allowed.
TRUSTED_FORMATS = {"json"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize *serialized_data* using the specified *deserialization_method*.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream to be deserialized.
    deserialization_method : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If *deserialization_method* is not in the list of trusted formats.
    """
    method = deserialization_method.lower()
    if method not in TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe deserialization method: '{deserialization_method}'. "
            f"Allowed methods: {', '.join(TRUSTED_FORMATS)}"
        )

    if method == "json":
        # json.loads expects a string, so decode the bytes safely.
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF‑8 encoded JSON.") from exc
        return json.loads(text)

    # If more formats are added in the future, they can be handled here.