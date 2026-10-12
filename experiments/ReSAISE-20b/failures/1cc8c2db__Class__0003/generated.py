import json
from typing import Any

# yaml is optional – if it’s not available we simply do not support it
try:
    import yaml  # type: ignore
except ImportError:   # pragma: no cover
    yaml = None

# List of signatures that are considered safe and trusted.
TRUSTED_SIGNATURES = {"json", "yaml"}

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize `data` according to the specified `signature`.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    signature : str
        The format of the serialized data. Supported values are 'json' and 'yaml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided signature is not in ``TRUSTED_SIGNATURES``.
    """
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature!r}")

    if signature == "json":
        # json.loads expects a str, so decode using UTF-8
        return json.loads(data.decode("utf-8"))

    if signature == "yaml":
        # yaml.safe_load is used to avoid executing arbitrary tags
        if yaml is None:  # pragma: no cover
            raise RuntimeError("yaml module is not installed")
        return yaml.safe_load(data.decode("utf-8"))

    # The code should never reach here because all supported signatures are handled
    raise RuntimeError("Unhandled signature logic error")