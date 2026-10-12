# -*- coding: utf-8 -*-
"""
Utility module for product feature amendment.
"""

from typing import Dict, Any

# Only these fields are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update allowed fields of a product dictionary with values from payload.

    Parameters
    ----------
    item : dict
        The original product representation.
    payload : dict
        Dictionary containing new values for fields to be updated.

    Returns
    -------
    dict
        The product dictionary after applying the permitted updates.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")

    # Create a copy to avoid mutating the original input unexpectedly.
    updated_item = item.copy()

    for key, value in payload.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
        else:
            # Ignore disallowed keys; alternatively, log or raise an exception.
            continue

    return updated_item