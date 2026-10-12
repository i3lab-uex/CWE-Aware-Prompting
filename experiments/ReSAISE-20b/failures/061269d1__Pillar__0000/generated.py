#!/usr/bin/env python3
"""
Product update helper.

This module defines a single public function `edit_product_info` which safely updates
a product dictionary. Only the keys listed in :data:`PERMITTED_FIELDS` are allowed to be
modified. All other fields remain untouched.

The function performs no side‑effects outside the supplied `item` dictionary and
does not expose or alter any nested objects that could represent resources such as
file handles or network sockets. This mitigates CWE‑664: Improper Control of a Resource
Through its Lifetime.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Allowed fields for modification
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with values from `details` for fields that are
    listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    item : dict
        The original product information dictionary.  It may contain any keys,
        but only the permitted fields will be updated.
    details : dict
        A dictionary containing key/value pairs that should be merged into
        `item`.  Keys not present in :data:`PERMITTED_FIELDS` are ignored.

    Returns
    -------
    dict
        The same dictionary object as `item`, updated in place.

    Notes
    -----
    * The function mutates the input `item` dictionary; it does not create a
      copy.  If callers need to preserve the original, they should pass a copy.
    * Only top‑level keys are considered.  Nested dictionaries or other
      structures inside the permitted fields are left untouched.
    * No validation of the new values is performed; callers should ensure
      type correctness before invoking this helper.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    for key in PERMITTED_FIELDS:
        if key in details:
            # Avoid accidental overwriting of non‑dict resources by ensuring the
            # new value is not a mutable object that could be shared elsewhere.
            # For this simple example we simply assign the value.
            item[key] = details[key]

    return item

# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     product = {"price": 19.99, "description": "A widget", "stock": 10}
#     updates = {"price": 17.49, "category": "gadgets", "unused": True}
#     print(edit_product_info(product, updates))