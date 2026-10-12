import json
import pickle
from typing import Any

# List of trusted serialization formats
TRUSTED_FORMATS = {"json", "text", "pickle"}

# Whitelist of safe modules/classes for pickle deserialization
SAFE_PICKLE_MODULES = {
    "builtins",
    # add more modules/classes if needed
}

class SafeUnpickler(pickle.Unpickler):
    """
    Unpickler that only allows loading objects from a restricted set of modules.
    """
    def find_class(self, module: str, name: str):
        if module not in SAFE_PICKLE_MODULES:
            raise pickle.UnpicklingError(
                f"Attempt to load disallowed module {module!r}"
            )
        return super().find_class(module, name)

def interpret_serialized_content(src_file: str, content_type: str) -> Any:
    """
    Deserialize data from a file in a safe manner.

    Parameters
    ----------
    src_file : str
        Path to the file containing serialized data.
    content_type : str
        Serialization format. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    if content_type not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {content_type!r}")

    try:
        with open(src_file, "rb") as f:
            raw_data = f.read()
    except OSError as exc:
        raise ValueError(f"Unable to read file {src_file!r}: {exc}") from exc

    if content_type == "text":
        # Decode as UTF-8; errors='strict' ensures invalid data raises
        return raw_data.decode("utf-8")

    if content_type == "json":
        try:
            text = raw_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data in {src_file!r}") from exc

    if content_type == "pickle":
        try:
            return SafeUnpickler(raw_data).load()
        except (pickle.UnpicklingError, EOFError) as exc:
            raise ValueError(f"Invalid or unsafe pickle data in {src_file!r}") from exc

    # Should never reach here because of the earlier check
    raise ValueError(f"Unhandled format: {content_type!r}")