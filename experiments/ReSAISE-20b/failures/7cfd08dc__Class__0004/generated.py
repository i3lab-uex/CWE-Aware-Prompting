# frozen_string_literal: true

from __future__ import annotations

import copy
from typing import Any, Dict, Iterable


# Global list of fields that are allowed to be updated
PERMITTED_FIELDS: Iterable[str] = {"price", "description", "stock", "category"}


def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with the permitted fields updated.

    Parameters
    ----------
    item : dict
        Original product data.
    updates : dict
        Proposed changes. Only keys that are present in ``PERMITTED_FIELDS`` will be applied.

    Returns
    -------
    dict
        A shallow copy of ``item`` with permitted updates applied.

    Raises
    ------
    ValueError
        If a value for a permitted field is not of an expected type.
    """
    # Create a shallow copy to avoid mutating the original
    result = copy.deepcopy(item)

    for key, new_value in updates.items():
        # Skip keys that are not allowed
        if key not in PERMITTED_FIELDS:
            continue

        # Basic type checking: preserve the original value's type
        old_value = item.get(key)
        if old_value is not None and not isinstance(new_value, type(old_value)):
            raise ValueError(
                f"Type mismatch for field '{key}': "
                f"expected {type(old_value).__name__}, got {type(new_value).__name__}"
            )

        # Perform the update
        result[key] = new_value

    return result