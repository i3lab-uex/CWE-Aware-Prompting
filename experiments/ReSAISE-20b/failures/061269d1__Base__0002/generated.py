# -*- coding: utf-8 -*-
"""
Utility to safely edit product information.

The module defines a single function `edit_product_info` that updates
only the attributes listed in the global ``PERMITTED_FIELDS`` list.
It guards against CWE-915 by ensuring that no other keys can be
modified, even if they are present in the incoming ``details`` dict.
"""

from __future__ import annotations

from typing import Dict, Any, List

# ----------------------------------------------------------------------
# Global configuration
# ----------------------------------------------------------------------
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
]

# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------
def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It may contain many keys, but only
        those in ``PERMITTED_FIELDS`` will be considered for modification.
    details : dict
        A dictionary of key/value pairs to apply as updates.

    Returns
    -------
    dict
        A new dictionary that contains the original data with the permitted
        updates applied.  The function never mutates the input ``item``.
    
    Raises
    ------
    ValueError
        If any key in ``details`` is not present in ``PERMITTED_FIELDS``.
    """
    # Create a shallow copy to avoid side effects
    updated_item = item.copy()

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Attempted to modify forbidden field '{key}'. "
                f"Only the following fields are allowed: {PERMITTED_FIELDS}"
            )
        updated_item[key] = value

    return updated_item