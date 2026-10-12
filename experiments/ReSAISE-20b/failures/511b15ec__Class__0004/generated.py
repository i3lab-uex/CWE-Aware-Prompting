# -*- coding: utf-8 -*-

"""
Utility module for product updates.
"""

from typing import Dict, Any

# Global list of fields that are allowed to be modified
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the product dictionary with new values from `change_data`.

    Only fields listed in :data:`PERMITTED_FIELDS` are allowed to be modified.
    The function modifies the original `prod` dictionary in place and returns it.

    Parameters
    ----------
    prod : dict
        Dictionary representing the product. It may contain arbitrary keys,
        but only those in :data:`PERMITTED_FIELDS` will be updated.
    change_data : dict
        Dictionary containing new values for the product fields.

    Returns
    -------
    dict
        The same dictionary instance as `prod`, updated with the permitted fields.

    Raises
    ------
    ValueError
        If `change_data` contains keys that are not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function performs a shallow update; nested structures are not deep‑merged.
    """
    # Validate that all keys in change_data are permitted
    disallowed = set(change_data) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Apply updates
    for key in PERMITTED_FIELDS:
        if key in change_data:
            prod[key] = change_data[key]

    return prod