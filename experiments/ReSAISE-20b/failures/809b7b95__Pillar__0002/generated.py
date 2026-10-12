#!/usr/bin/env python3
"""
Utility to safely modify product details.

The module defines a single public function `modify_item_details` that updates
a product dictionary in an immutable fashion, only applying changes for keys
listed in the global `PERMITTED_FIELDS`.  The function performs basic type
validation and avoids side‑effects on the original product dictionary.

Security considerations:
- Only permitted fields are updated, preventing accidental or malicious
  changes to sensitive attributes.
- The function returns a new dictionary instance, so callers cannot
  unintentionally modify the original product.
- Input values are not blindly cast; a ValueError is raised if an update
  value is of an incompatible type.
"""

from copy import deepcopy
from typing import Dict, Any

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def _validate_field_value(field: str, value: Any) -> None:
    """
    Validate that the new value for a field is of an acceptable type.

    Raises ValueError if validation fails.
    """
    if field == "price":
        if not isinstance(value, (int, float)):
            raise ValueError(f"Invalid type for 'price': {type(value).__name__}")
    elif field == "description":
        if not isinstance(value, str):
            raise ValueError(f"Invalid type for 'description': {type(value).__name__}")
    elif field == "stock":
        if not isinstance(value, int):
            raise ValueError(f"Invalid type for 'stock': {type(value).__name__}")
    elif field == "category":
        if not isinstance(value, str):
            raise ValueError(f"Invalid type for 'category': {type(value).__name__}")
    else:
        # This case should never occur because we filter by PERMITTED_FIELDS
        raise ValueError(f"Field '{field}' is not permitted for update.")


def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied to permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary.
    details : dict
        Dictionary of intended updates. Only keys in PERMITTED_FIELDS are applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.

    Raises
    ------
    ValueError
        If any provided update value is of an incompatible type.
    """
    # Make a deep copy to avoid mutating the original product
    updated_item = deepcopy(item)

    for key, new_value in details.items():
        if key not in PERMITTED_FIELDS:
            # Skip any disallowed field silently; could also log or raise if desired
            continue

        _validate_field_value(key, new_value)
        updated_item[key] = new_value

    return updated_item