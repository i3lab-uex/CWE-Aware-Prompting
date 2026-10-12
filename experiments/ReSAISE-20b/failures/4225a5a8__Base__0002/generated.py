import json
import xml.etree.ElementTree as ET
import pickle
from typing import Any

# --------------------------------------------------------------------------- #
# Safe deserialization utilities
# --------------------------------------------------------------------------- #

def _safe_pickle_loads(data: bytes) -> Any:
    """
    Deserialize pickle data while preventing the execution of arbitrary code.
    Only allows built-in types (int, float, str, list, dict, tuple, set, bool, None).
    """
    class SafeUnpickler(pickle.Unpickler):
        def find_class(self, module: str, name: str):
            # Only allow built-in modules
            if module != "builtins":
                raise pickle.UnpicklingError(f"Disallowed module {module}")
            # Allow only safe built-in types
            if name in {"int", "float", "str", "list", "dict",
                         "tuple", "set", "bool", "NoneType"}:
                return getattr(__builtins__, name)
            raise pickle.UnpicklingError(f"Disallowed type {name}")

    return SafeUnpickler(io.BytesIO(data)).load()

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize `raw_data` according to the specified `method_name`.

    Supported formats: 'json', 'xml', 'pickle'.
    Raises ValueError for unsupported or dangerous formats.
    """
    if not isinstance(raw_data, (bytes, bytearray)):
        raise ValueError("raw_data must be bytes-like")

    method = method_name.lower()

    if method == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method == "xml":
        try:
            # Parse XML into an ElementTree element
            return ET.fromstring(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    elif method == "pickle":
        # Use a safe unpickler that only allows built-in types
        try:
            return _safe_pickle_loads(raw_data)
        except (pickle.UnpicklingError, EOFError) as exc:
            raise ValueError("Invalid or unsafe pickle data") from exc

    else:
        raise ValueError(f"Unsupported serialization method: {method_name}")