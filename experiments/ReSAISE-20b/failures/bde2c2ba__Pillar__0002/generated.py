#!/usr/bin/env python3
"""
Module: product_updater

Provides a function to safely update allowed fields of a product dictionary.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable


# Global list of fields that may be updated.
PERMITTED_FIELDS: Iterable[str] = ("price", "description", "stock", "category")


def update_item_information(
    product_info: Dict[str, Any],
    new_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    product_info : dict
        Original product data. Must be a mapping of string keys to values.
    new_data : dict
        Desired updates. Keys are field names; values are the new data.

    Returns
    -------
    dict
        A shallow copy of ``product_info`` with permitted fields updated.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    KeyError
        If ``new_data`` contains keys that are not in :data:`PERMITTED_FIELDS`.
    ValueError
        If a permitted field is updated with an incompatible type
        (e.g., non‑numeric value for ``price`` or ``stock``).

    Notes
    -----
    * The original ``product_info`` is not mutated.
    * Only fields listed in :data:`PERMITTED_FIELDS` may be changed.
    * Basic type checks are performed to avoid obvious data corruption.

    Example
    -------
    >>> product = {"price": 10.0, "description": "Item", "stock": 5, "category": "A"}
    >>> updates = {"price": 12.5, "stock": 4}
    >>> update_item_information(product, updates)
    {'price': 12.5, 'description': 'Item', 'stock': 4, 'category': 'A'}
    """
    # Validate input types
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Ensure new_data only contains permitted fields
    for key in new_data:
        if key not in PERMITTED_FIELDS:
            raise KeyError(f"Field '{key}' is not permitted for update")

    # Perform basic type validation for numeric fields
    numeric_fields = {"price", "stock"}
    for key, value in new_data.items():
        if key in numeric_fields:
            # Allow int or float for price and stock
            if not isinstance(value, (int, float)):
                raise ValueError(f"Field '{key}' must be a number")

    # Create a shallow copy to avoid mutating the original
    updated_product = copy.copy(product_info)

    # Apply updates
    for key, value in new_data.items():
        updated_product[key] = value

    return updated_product