# -*- coding: utf-8 -*-

"""
Product modification module.

This module provides a single public function `modify_item_details` which updates
a product dictionary in-place only for attributes that are allowed to be changed.
The list of fields that may be modified is defined in the global constant
`PERMITTED_FIELDS`.  Any attempt to modify a disallowed field raises a
``ValueError``.

The implementation is defensive: it works with any mapping-like object that
supports the ``dict`` interface and returns a new dictionary instance rather
than mutating the input directly.  This avoids accidental side‑effects on
objects that are shared elsewhere in an application.
"""

from __future__ import annotations

import copy
from typing import Dict, Iterable


# --------------------------------------------------------------------------- #
# Configuration – list of attributes that are allowed to be modified
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_item_details(item: Dict, details: Dict) -> Dict:
    """
    Update a product dictionary with values from *details* only for
    attributes that are present in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    item :
        A mapping representing the current product state.
    details :
        A mapping containing key/value pairs to be applied as updates.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.

    Raises
    ------
    ValueError
        If *details* contains any key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function does **not** modify the input ``item``; instead it returns a
    new dictionary.  This protects callers from unintended mutation of shared
    data structures.
    """
    # Defensive copy to avoid mutating the original item
    updated_item = copy.deepcopy(item)

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not permitted to be updated. "
                f"Allowed fields: {sorted(PERMITTED_FIELDS)}"
            )
        updated_item[key] = value

    return updated_item