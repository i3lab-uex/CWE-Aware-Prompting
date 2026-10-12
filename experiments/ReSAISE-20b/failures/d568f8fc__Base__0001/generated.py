# -*- coding: utf-8 -*-
"""
Module providing a safe product data updater.
"""

from typing import Dict, Any

# Only these keys are allowed to be modified.  Add or remove as needed.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def adjust_product_data(prod_info: Dict[str, Any], change_vals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        Dictionary representing the product.  The dictionary is updated in place.
    change_vals : dict
        Dictionary containing new values for fields that should be updated.

    Returns
    -------
    dict
        The updated product dictionary (same object as ``prod_info``).

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If ``change_vals`` contains keys that are not in :data:`PERMITTED_FIELDS`.
    """
    if not isinstance(prod_info, dict):
        raise TypeError(f"prod_info must be a dict, got {type(prod_info).__name__}")
    if not isinstance(change_vals, dict):
        raise TypeError(f"change_vals must be a dict, got {type(change_vals).__name__}")

    # Reject any attempts to modify non‑permitted fields
    invalid_keys = set(change_vals) - PERMITTED_FIELDS
    if invalid_keys:
        raise ValueError(f"Attempted to modify disallowed fields: {sorted(invalid_keys)}")

    # Apply the permitted changes
    for key, value in change_vals.items():
        prod_info[key] = value

    return prod_info