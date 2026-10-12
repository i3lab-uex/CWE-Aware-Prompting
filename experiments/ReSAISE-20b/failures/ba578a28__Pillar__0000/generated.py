# -*- coding: utf-8 -*-
"""
Product data modification module.

This module provides a single public function, `modify_product_data`, which
updates product attributes in a safe and controlled manner. Only the fields
listed in `PERMITTED_FIELDS` may be modified; all other keys are ignored.
The function returns a new dictionary instance so that the original product
data is left untouched, preventing accidental side‑effects.

CWE-664: The implementation avoids improper control of resources by ensuring
that no external resource (e.g. a file handle or network socket) is opened,
held, or closed during the update process. All operations are purely
in‑memory and stateless.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

#: Fields that are allowed to be modified.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_product_data(
    product_details: Dict[str, Any],
    update_info: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied to permitted fields.

    Parameters
    ----------
    product_details : dict
        The original product data. This dictionary is **not** modified.
    update_info : dict
        A mapping of field names to new values. Only keys that are present in
        :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the original product data with any permitted
        updates applied.

    Raises
    ------
    TypeError
        If either argument is not a mapping type.
    ValueError
        If `product_details` does not contain one of the permitted fields that is
        attempted to be updated. This ensures callers are aware of missing keys.

    Notes
    -----
    - The function performs a deep copy of the original product data to avoid
      accidental mutation of nested mutable objects.
    - Only the fields explicitly listed in :data:`PERMITTED_FIELDS` are
      considered; all other keys in ``update_info`` are silently ignored.
    """
    # Validate inputs
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Create a deep copy to avoid mutating the original product data
    updated_product = deepcopy(product_details)

    # Apply permitted updates
    for field, new_value in update_info.items():
        if field not in PERMITTED_FIELDS:
            # Ignore disallowed fields
            continue

        if field not in updated_product:
            raise ValueError(
                f"Attempted to update missing field '{field}' in product_details"
            )

        updated_product[field] = new_value

    return updated_product


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_product = {
        "price": 19.99,
        "description": "A great widget",
        "stock": 100,
        "category": "gadgets",
    }

    updates = {
        "price": 17.49,
        "stock": 120,
        "color": "red",          # not permitted, will be ignored
    }

    print("Original:", sample_product)
    modified = modify_product_data(sample_product, updates)
    print("Modified:", modified)