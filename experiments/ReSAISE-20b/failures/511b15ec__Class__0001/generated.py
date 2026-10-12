# -*- coding: utf-8 -*-
"""
Utility module for updating product information safely.
"""

from typing import Dict, Any

# List of fields that are allowed to be updated
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod : dict
        The original product dictionary. It is modified in place.
    change_data : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated product dictionary (same object as ``prod``).

    Notes
    -----
    Only keys that are present in :data:`PERMITTED_FIELDS` will be applied.
    Any other keys in ``change_data`` are silently ignored to prevent accidental
    modification of sensitive or internal attributes.

    Examples
    --------
    >>> product = {'price': 10.0, 'description': 'Old', 'stock': 5}
    >>> update_product_info(product, {'price': 12.0, 'stock': 10})
    {'price': 12.0, 'description': 'Old', 'stock': 10}
    >>> update_product_info(product, {'nonexistent': 42})  # ignored
    {'price': 12.0, 'description': 'Old', 'stock': 10}
    """
    # Ensure the inputs are dictionaries to avoid accidental type errors
    if not isinstance(prod, dict):
        raise TypeError("prod must be a dictionary")
    if not isinstance(change_data, dict):
        raise TypeError("change_data must be a dictionary")

    for key, value in change_data.items():
        if key in PERMITTED_FIELDS:
            prod[key] = value
    return prod