#!/usr/bin/env python3
"""
Secure product feature amendment module.

This module defines a single function, `amend_product_features`, which updates
a product dictionary with new values provided in a payload. Only fields listed
in the globally defined `PERMITTED_FIELDS` are allowed to be modified.

The implementation follows CWE‑915 guidelines by explicitly validating each
field name before performing any assignment, thereby preventing unauthorized
or unintended attribute changes.
"""

from __future__ import annotations

import copy
from typing import Dict, Iterable, Any


# --------------------------------------------------------------------------- #
# Configuration: list of fields that are allowed to be amended.
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from *payload*.

    Only fields listed in the global ``PERMITTED_FIELDS`` are allowed to be
    modified.  The function returns a new dictionary containing the updated
    values, leaving the original *item* untouched.

    Parameters
    ----------
    item : dict
        The original product dictionary.  Must contain keys corresponding to
        the product attributes.
    payload : dict
        A dictionary of fields to update.  Only keys that exist in
        ``PERMITTED_FIELDS`` will be applied.

    Returns
    -------
    dict
        A new dictionary reflecting the updated product data.

    Raises
    ------
    ValueError
        If *payload* contains any keys that are not in ``PERMITTED_FIELDS``.
    """
    # Validate payload keys against the permitted list
    disallowed = [k for k in payload if k not in PERMITTED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed)}"
        )

    # Create a shallow copy of the original item to avoid side effects
    updated_item = copy.deepcopy(item)

    # Apply permitted updates
    for key, value in payload.items():
        updated_item[key] = value

    return updated_item


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    original_product = {
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 42,
        "category": "electronics",
    }

    new_data = {
        "price": 17.99,
        "stock": 50,
    }

    try:
        updated = amend_product_features(original_product, new_data)
        print("Updated product:", updated)
    except ValueError as exc:
        print(f"Error: {exc}")