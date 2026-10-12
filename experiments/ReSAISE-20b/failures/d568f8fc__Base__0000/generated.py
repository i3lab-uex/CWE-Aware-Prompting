# -*- coding: utf-8 -*-
"""
Utility module for safely updating product data.

The function `adjust_product_data` updates only the fields listed in
the globally defined `PERMITTED_FIELDS`.  Any attempt to modify a field
outside this whitelist raises a ValueError, preventing accidental or
malicious changes to the product dictionary.

CWE-915 (Improperly Controlled Modification of Dynamically-Determined
Object Attributes) is mitigated by strict attribute whitelisting.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# Whitelisted fields that are allowed to be updated
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


def adjust_product_data(prod_info: Dict[str, Any], change_vals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values while enforcing
    permission checks on the fields that can be modified.

    Parameters
    ----------
    prod_info : dict
        The original product dictionary. Keys represent product attributes.
    change_vals : dict
        Dictionary of new values keyed by attribute name.

    Returns
    -------
    dict
        A shallow copy of `prod_info` with the permitted changes applied.

    Raises
    ------
    ValueError
        If `change_vals` contains a key that is not in `PERMITTED_FIELDS`.
    """
    # Create a shallow copy to avoid mutating the original input
    updated_product = prod_info.copy()

    for key, new_value in change_vals.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not permitted for update. "
                f"Allowed fields: {', '.join(sorted(PERMITTED_FIELDS))}"
            )
        updated_product[key] = new_value

    return updated_product