# -*- coding: utf-8 -*-
"""
Product update module.

This module defines a single public function, ``update_product_info``, that
updates only the fields listed in the globally defined ``PERMITTED_FIELDS``.
The function raises a ``ValueError`` if an attempt is made to modify any
non‑permitted field, thereby guarding against unintended changes and
protecting the product data integrity.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# List of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the fields of a product dictionary with values from ``change_data``.
    
    Only keys present in :data:`PERMITTED_FIELDS` may be modified.  Any attempt
    to modify a non‑permitted field will raise a ``ValueError``.
    
    Parameters
    ----------
    prod : dict
        The product dictionary to be updated.  It is modified in place.
    change_data : dict
        A mapping of field names to new values that should be applied.
    
    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).
    
    Raises
    ------
    ValueError
        If ``change_data`` contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    
    # Validate the incoming data
    for key in change_data:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted to be updated.")
    
    # Perform the update
    prod.update(change_data)
    
    return prod