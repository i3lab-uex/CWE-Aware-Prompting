# -*- coding: utf-8 -*-
"""
Utility module for safely updating product details.

This implementation follows best practices to avoid CWE‑915:
only a whitelisted set of fields (PERMITTED_FIELDS) can be modified.
"""

from copy import deepcopy
from typing import Dict, Iterable

# Global whitelist of fields that are allowed to be updated.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

def modify_product_details(product: Dict[str, any], data: Dict[str, any]) -> Dict[str, any]:
    """
    Update a product dictionary with new values from ``data``.
    
    Parameters
    ----------
    product : dict
        The original product dictionary.  It is not modified in place.
    data : dict
        Dictionary containing keys and values to update the product with.
    
    Returns
    -------
    dict
        A new dictionary containing the updated product details.
    
    Raises
    ------
    TypeError
        If ``product`` or ``data`` is not a dictionary.
    KeyError
        If an attempt is made to update a field that is not in ``PERMITTED_FIELDS``.
    """
    
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Create a shallow copy to avoid mutating the original product
    updated_product = deepcopy(product)

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise KeyError(f"Field '{key}' is not permitted to be updated.")
        # Perform a simple type check or conversion if necessary
        # (example: ensure price is numeric, stock is int)
        if key == "price":
            try:
                value = float(value)
            except (TypeError, ValueError):
                raise ValueError("price must be a numeric value")
        elif key == "stock":
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValueError("stock must be an integer")
        # Update the allowed field
        updated_product[key] = value

    return updated_product