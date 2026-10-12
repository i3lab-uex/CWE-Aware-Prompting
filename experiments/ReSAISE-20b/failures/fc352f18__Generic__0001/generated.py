# -*- coding: utf-8 -*-
"""
Utility module for safely updating product dictionaries.
"""

from typing import Dict, Any

# Define the fields that are allowed to be updated.  Add or remove
# items from this list as your application evolves.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from ``payload`` only if the
    keys are present in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    item :
        The original product dictionary.  It is mutated in place.
    payload :
        Dictionary containing proposed updates.

    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).

    Notes
    -----
    * Unknown keys are silently ignored to avoid accidental injection of
      arbitrary fields.
    * The function does not perform type validation; callers should ensure
      that the payload values are of the expected types.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary representing the product.")
    if not isinstance(payload, dict):
        raise TypeError("`payload` must be a dictionary of updates.")

    for key, value in payload.items():
        if key in PERMITTED_FIELDS:
            item[key] = value

    return item