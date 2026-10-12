# -*- coding: utf-8 -*-
"""
Utility module for safely updating product data.

The `adjust_product_data` function updates only the fields that are
explicitly allowed by the global `PERMITTED_FIELDS` list.  This protects
against CWE-915: *Improperly Controlled Modification of Dynamically-
Determined Object Attributes*.
"""

from __future__ import annotations

from typing import Dict, Any, Mapping


# List of fields that may be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]


def adjust_product_data(
    prod_info: Mapping[str, Any], change_vals: Mapping[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for allowed fields.

    Parameters
    ----------
    prod_info : Mapping[str, Any]
        The original product data.  It may be any mapping (e.g., a dict)
        that contains product attributes.
    change_vals : Mapping[str, Any]
        A mapping of field names to new values that should be applied.

    Returns
    -------
    Dict[str, Any]
        A new dictionary containing the updated product data.

    Raises
    ------
    KeyError
        If `change_vals` contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    # Create a copy so we do not mutate the caller's data.
    updated = dict(prod_info)

    permitted_set = set(PERMITTED_FIELDS)
    for key, value in change_vals.items():
        if key not in permitted_set:
            raise KeyError(
                f"Attempted to modify non‑permitted field '{key}'. "
                "Only the following fields are allowed: "
                f"{', '.join(sorted(permitted_set))}"
            )
        updated[key] = value

    return updated