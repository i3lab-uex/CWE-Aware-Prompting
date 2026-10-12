# SPDX-License-Identifier: MIT

"""
Utility module for updating product attributes safely.

The global `PERMITTED_FIELDS` list defines which fields can be
modified.  The function ``update_product_attributes`` takes an existing
product dictionary and a dictionary of desired updates, applies only the
permitted changes, and returns a new dictionary representing the updated
product.

The original product dictionary is left untouched to avoid accidental side‑effects.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied only to permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary.
    updates : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        A new dictionary representing the updated product.

    Raises
    ------
    ValueError
        If ``updates`` contains keys that are not in ``PERMITTED_FIELDS``.

    Notes
    -----
    - The function does **not** modify the original ``item`` dictionary.
    - Only keys present in ``PERMITTED_FIELDS`` are accepted; all others raise
      an exception to guard against accidental data leaks or typos.
    """
    # Validate that all requested updates are permitted
    invalid_keys = [k for k in updates if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_keys)}"
        )

    # Create a shallow copy to avoid mutating the original product
    updated_item = copy.deepcopy(item)

    # Apply updates
    for key, value in updates.items():
        updated_item[key] = value

    return updated_item