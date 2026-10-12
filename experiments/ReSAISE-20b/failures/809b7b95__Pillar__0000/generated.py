# -*- coding: utf-8 -*-
"""
Utility to modify product details while enforcing a whitelist of permitted fields.

The module intentionally avoids side‑effects on the original `item` by working on a shallow copy.
"""

from __future__ import annotations

# Global whitelist of fields that may be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_item_details(item: dict, details: dict) -> dict:
    """
    Return a new product dictionary with updates applied only to fields
    listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    item : dict
        Original product representation. The function does not modify this object.
    details : dict
        Mapping of desired updates. Keys not in :data:`PERMITTED_FIELDS`
        are silently ignored.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.

    Notes
    -----
    * The function performs a shallow copy of `item`; nested mutable objects are shared.
      This is sufficient for typical product data structures where values are primitives.
    * The function does **not** raise an exception for disallowed keys; they are simply ignored.
      If stricter validation is required, replace the `if key in PERMITTED_FIELDS` check with
      a more explicit error handling strategy.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Create a shallow copy to avoid mutating the original item.
    updated_item = dict(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item