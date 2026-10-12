import json
from typing import Any

# Import only the safe loader from PyYAML to avoid arbitrary code execution
try:
    import yaml  # type: ignore
except ImportError as exc:
    raise RuntimeError("PyYAML is required for YAML deserialization") from exc

# List of trusted formats that are considered safe
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize *data* according to the specified *signature*.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    signature : str
        Format of the serialized data. Supported values are those in
        TRUSTED_SIGNATURES.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *signature* is not in TRUSTED_SIGNATURES.
    """
    sig = signature.lower()
    if sig not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    if sig == "json":
        # json.loads expects a string, so decode using UTF-8
        return json.loads(data.decode("utf-8"))
    elif sig == "yaml":
        # yaml.safe_load prevents arbitrary object construction
        return yaml.safe_load(data.decode("utf-8"))
    else:
        # This block is theoretically unreachable due to the earlier check,
        # but keeps type-checkers happy.
        raise ValueError(f"Unsupported format: {signature}")