# -*- coding: utf-8 -*-

"""
Utility to update product details with strict field permissions.

The module defines a global list `PERMITTED_FIELDS` that enumerates
the only product attributes that may be modified.  The function
`modify_item_details` takes an existing product dictionary and a
dictionary of desired updates, applies the changes only for fields
present in `PERMITTED_FIELDS`, and returns a new dictionary with
the updated state.  No dynamic code execution or unsafe operations
are performed, mitigating CWE‑913 risks.
"""

from __future__ import annotations

# List of product attributes that are allowed to be modified
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def modify_item_details(item: dict, details: dict) -> dict:
    """
    Return a new product dictionary with updates applied only to
    permitted fields.

    Parameters
    ----------
    item : dict
        The original product representation.  It is treated as read‑only;
        a new dictionary will be returned.
    details : dict
        Key/value pairs representing the desired updates.  Only keys that
        exist in ``PERMITTED_FIELDS`` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the original product data with
        updates applied for permitted fields.

    Raises
    ------
    TypeError
        If either ``item`` or ``details`` is not a mapping type.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Create a shallow copy of the original item to avoid mutating it
    updated_item = dict(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item