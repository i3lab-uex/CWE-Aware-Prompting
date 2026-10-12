# -*- coding: utf-8 -*-
"""
Utility module for updating product information.

The module defines a single public function, `update_item_information`, which
updates a product dictionary with new values for a predefined set of fields.
Only the keys listed in `PERMITTED_FIELDS` are allowed to be updated; any
other keys present in the update payload are silently ignored.

The function mutates the input `product_info` dictionary and returns it.
"""

from __future__ import annotations

from typing import Dict, Any

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_information(product_info: Dict[str, Any],
                             new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update product information with new data.

    Parameters
    ----------
    product_info : dict
        Dictionary representing the current state of a product.
    new_data : dict
        Dictionary containing key-value pairs with updates.

    Returns
    -------
    dict
        The same dictionary object as `product_info`, now containing any
        updates that were permitted.

    Notes
    -----
    * Only keys present in :data:`PERMITTED_FIELDS` are applied.
    * The function modifies `product_info` in place and returns it for
      convenience.  If you need to preserve the original dictionary, pass a
      shallow copy.
    """
    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            product_info[key] = value
    return product_info