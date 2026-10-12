import json
import pickle
from pathlib import Path
from typing import Any


# Define the whitelist of safe formats.
SAFE_FORMATS = {"json", "text", "pickle"}


class RestrictedUnpickler(pickle.Unpickler):
    """
    A pickle.Unpickler that only allows safe, built‑in objects.
    This implementation forbids the creation of arbitrary classes
    and modules to mitigate code execution attacks.
    """

    def find_class(self, module: str, name: str):
        # Only allow built-in types and modules that are explicitly whitelisted.
        allowed_builtins = {
            "builtins",
            # Add other safe modules here if needed.
        }
        if module not in allowed_builtins:
            raise pickle.UnpicklingError(
                f"Attempted to load unsafe module '{module}'."
            )
        # For builtins, we can safely allow the requested name.
        return super().find_class(module, name)


def process_serialfile(input_path: str | Path, format_type: str) -> Any:
    """
    Deserialize a file's contents using only trusted formats.

    Parameters
    ----------
    input_path : str | Path
        Path to the serialized file.
    format_type : str
        The serialization format. Must be one of SAFE_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS.
    FileNotFoundError, PermissionError
        Propagated if the file cannot be accessed.
    """
    format_type = format_type.lower()
    if format_type not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or untrusted format '{format_type}'. "
            f"Allowed formats: {', '.join(SAFE_FORMATS)}"
        )

    path = Path(input_path)

    if format_type == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if format_type == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    # format_type == "pickle"
    with path.open("rb") as f:
        return RestrictedUnpickler(f).load()