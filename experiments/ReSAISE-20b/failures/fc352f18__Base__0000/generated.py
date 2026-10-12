# -*- coding: utf-8 -*-
"""
Product feature amendment module.

This module defines a single public function, ``amend_product_features``, that
updates only the fields listed in :data:`PERMITTED_FIELDS`.  All other keys in
the supplied payload are ignored to guard against CWE‑915
(Improperly Controlled Modification of Dynamically-Determined Object Attributes).
"""

from __future__ import annotations

from typing import Dict, Iterable

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

#: The list of attributes that may be updated by external callers.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def amend_product_features(item: Dict[str, object], payload: Dict[str, object]) -> Dict[str, object]:
    """
    Update an existing product dictionary with values from *payload*.

    Only keys that are present in :data:`PERMITTED_FIELDS` will be modified.
    All other entries in *payload* are ignored, preventing accidental
    modification of protected attributes.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It will be updated in place.
    payload : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The same dictionary object that was passed in, now updated with the
        permitted changes.

    Raises
    ------
    TypeError
        If either *item* or *payload* is not a mapping.
    """
    if not isinstance(item, dict):
        raise TypeError(f"item must be a dict, got {type(item).__name__}")
    if not isinstance(payload, dict):
        raise TypeError(f"payload must be a dict, got {type(payload).__name__}")

    # Iterate over the payload and update only permitted keys.
    for key, value in payload.items():
        if key in PERMITTED_FIELDS:
            item[key] = value
    return item

# --------------------------------------------------------------------------- #
# End of module
# --------------------------------------------------------------------------- #