# -*- coding: utf-8 -*-
"""
Utility for safely updating product attributes.

The module defines a global list `PERMITTED_FIELDS` containing the
attribute names that are allowed to be updated. The function
`amend_product_features` applies only those updates from a supplied
payload dictionary to the product item, leaving all other fields intact.
"""

from __future__ import annotations

from typing import Dict, Any

# Only these fields may be modified.  Add or remove names as required.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from *payload*.

    Parameters
    ----------
    item : dict
        The original product representation. It is modified in place.
    payload : dict
        A dictionary containing new values for the fields to be updated.

    Returns
    -------
    dict
        The modified product dictionary.

    Notes
    -----
    * Only keys present in :data:`PERMITTED_FIELDS` are applied.
    * The function does not create a new dictionary; it mutates the
      original `item` for efficiency and to preserve any references.
    * If a key in `payload` is not permitted, it is silently ignored
      to avoid accidental injection of disallowed attributes.
    """
    # Guard against mutation of non-dict inputs
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(payload, dict):
        raise TypeError(f"Expected 'payload' to be a dict, got {type(payload).__name__}")

    for key, value in payload.items():
        if key in PERMITTED_FIELDS:
            item[key] = value
    return item