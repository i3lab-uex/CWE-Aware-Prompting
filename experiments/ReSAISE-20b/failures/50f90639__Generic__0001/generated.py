#!/usr/bin/env python3
"""
Utility module for updating product details.

The `modify_product_details` function ensures that only a whitelisted set of fields
(`PERMITTED_FIELDS`) can be updated.  Any attempt to modify a non‑permitted field
raises a `ValueError`.  The function performs a shallow update – it does not
deep‑copy nested structures, but that is typically sufficient for product
metadata.

Author: ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any, List

# Global whitelist of fields that may be updated.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
    "brand",
    "sku",
    "weight",
]

def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from ``data``.

    Parameters
    ----------
    product : dict
        The original product dictionary.  This dictionary is updated in place.
    data : dict
        A mapping of field names to new values.  Only keys present in
        ``PERMITTED_FIELDS`` will be applied.

    Returns
    -------
    dict
        The updated product dictionary (the same object as ``product``).

    Raises
    ------
    ValueError
        If any key in ``data`` is not listed in ``PERMITTED_FIELDS``.

    Examples
    --------
    >>> prod = {"price": 10.0, "stock": 5}
    >>> modify_product_details(prod, {"price": 12.0, "stock": 4})
    {'price': 12.0, 'stock': 4}
    >>> modify_product_details(prod, {"price": 15.0, "color": "red"})
    Traceback (most recent call last):
        ...
    ValueError: Attempted to modify non‑permitted field 'color'.
    """
    # Validate input types for robustness.
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Attempted to modify non‑permitted field '{key}'.")
        product[key] = value

    return product