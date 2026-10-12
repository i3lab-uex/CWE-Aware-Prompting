# -*- coding: utf-8 -*-
"""
Utility to safely update product information.
"""

from typing import Dict, Any

# Fields that are allowed to be updated
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from *change_data*.

    Only keys listed in the global ``PERMITTED_FIELDS`` are applied.  Any
    other keys are ignored, ensuring that untrusted input cannot modify
    arbitrary attributes.

    Parameters
    ----------
    prod : dict
        The original product dictionary.  It is modified in place and also
        returned for convenience.
    change_data : dict
        Dictionary containing new values for fields to be updated.

    Returns
    -------
    dict
        The product dictionary after applying permitted changes.

    Raises
    ------
    TypeError
        If either *prod* or *change_data* is not a dictionary.
    """
    if not isinstance(prod, dict):
        raise TypeError(f"Expected prod to be a dict, got {type(prod).__name__}")
    if not isinstance(change_data, dict):
        raise TypeError(f"Expected change_data to be a dict, got {type(change_data).__name__}")

    for key, value in change_data.items():
        if key in PERMITTED_FIELDS:
            prod[key] = value
    return prod