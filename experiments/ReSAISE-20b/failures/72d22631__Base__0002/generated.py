import json
from typing import Any, Union

# List of serialization methods considered safe for this context.
_TRUSTED_METHODS = {"json"}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Restore a Python object from serialized bytes.

    Parameters
    ----------
    deserialized_bytes : bytes
        The byte stream containing the serialized data.
    method_for_serialization : str
        The serialization format used, e.g. 'json'.

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested serialization method is not in the trusted list.
    """
    # Normalise the method name to avoid case‑sensitivity issues
    method = method_for_serialization.strip().lower()

    if method not in _TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or potentially harmful serialization method: '{method_for_serialization}'"
        )

    # Currently only JSON is supported; the implementation can be extended
    # for other safe formats as needed.
    if method == "json":
        try:
            decoded = deserialized_bytes.decode("utf-8")
            return json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    # If additional methods are added later, handle them here.