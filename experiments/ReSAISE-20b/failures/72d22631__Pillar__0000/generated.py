import json
from typing import Any

# List of trusted serialization formats
TRUSTED_METHODS = {"json"}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only trusted methods.

    Parameters
    ----------
    deserialized_bytes : bytes
        The serialized data to be recovered.
    method_for_serialization : str
        The serialization format used (e.g., 'json').

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the specified serialization method is unsupported or potentially unsafe.
    """
    if not isinstance(deserialized_bytes, (bytes, bytearray)):
        raise ValueError("Input must be bytes or bytearray.")

    method = method_for_serialization.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe serialization method: {method_for_serialization}")

    # Currently only JSON is supported; add additional safe formats here if needed
    try:
        decoded = deserialized_bytes.decode("utf-8")
        return json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Failed to deserialize data.") from exc