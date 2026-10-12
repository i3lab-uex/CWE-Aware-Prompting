import json
import pickle
from typing import Any

# List of trusted serialization formats
TRUSTED_SIGNATURES = {"json", "yaml", "pickle"}

def deserialize_data(data: bytes, signature: str) -> Any:
    """
    Deserialize data from an untrusted source only if the format is trusted.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    signature : str
        The format of the serialized data (e.g., 'json', 'yaml', or 'pickle').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided signature is not in the list of trusted formats.
    """
    if signature not in TRUSTED_SIGNATURES:
        raise ValueError(f"Unsupported format: {signature}")

    if signature == "json":
        # JSON is safe for deserialization
        return json.loads(data.decode("utf-8"))

    if signature == "yaml":
        # Use safe loader to avoid arbitrary code execution
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("PyYAML is required for YAML deserialization") from exc
        return yaml.safe_load(data.decode("utf-8"))

    if signature == "pickle":
        # Pickle is inherently unsafe; only deserialize if the data comes from a trusted source.
        # In this implementation, we assume that the caller has already verified trust.
        return pickle.loads(data)

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {signature}")