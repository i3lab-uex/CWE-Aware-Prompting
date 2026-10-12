# -*- coding: utf-8 -*-
"""
Utility module for safely updating product dictionaries.

The global `PERMITTED_FIELDS` list controls which attributes of a product
may be modified.  This module guards against CWE‑915 by ensuring that only
explicitly permitted keys are written to the product dictionary.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Define the fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from `change_data`.

    Only keys that are present in the global ``PERMITTED_FIELDS`` list
    will be applied.  If a key is not permitted, a ``ValueError`` is raised.

    Parameters
    ----------
    prod : dict
        The original product dictionary.  It is **not** modified in place;
        a shallow copy with the updates applied is returned.
    change_data : dict
        Dictionary containing fields to update.  Keys that are not in
        ``PERMITTED_FIELDS`` cause an exception.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.
    """
    if not isinstance(prod, dict):
        raise TypeError("prod must be a dictionary")
    if not isinstance(change_data, dict):
        raise TypeError("change_data must be a dictionary")

    # Make a shallow copy so the original product remains unchanged.
    updated_prod = copy.deepcopy(prod)

    for key, value in change_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")
        # Optional: add type checks here if required
        updated_prod[key] = value

    return updated_prod