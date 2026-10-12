# -*- coding: utf-8 -*-
"""
Product update helper.

This module provides a single public function, :func:`edit_product_info`,
which updates only a predefined set of product attributes.  The function
is deliberately defensive: it validates its arguments, ignores any
attempts to modify disallowed keys, and returns a new dictionary rather
than mutating the input in place.  This protects against CWE‑915:
Improperly Controlled Modification of Dynamically‑Determined Object
Attributes.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Only these keys are allowed to be modified.  Add or remove as needed.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with permitted fields from ``details``.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It must be a mapping of string keys
        to arbitrary values.
    details : dict
        A dictionary containing key/value pairs intended for update.  Only
        keys that are present in :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.  The
        original ``item`` is left untouched.

    Raises
    ------
    TypeError
        If either ``item`` or ``details`` is not a dictionary.
    ValueError
        If ``PERMITTED_FIELDS`` contains non‑string entries (a configuration
        error).

    Notes
    -----
    * The function does **not** perform type validation on the values.
      If stricter checks are required, they should be added here.

    * This function is intentionally safe against attempts to modify
      disallowed attributes, mitigating CWE‑915.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Defensive copy to avoid mutating the caller's data
    updated = item.copy()

    permitted_set = set(PERMITTED_FIELDS)
    if not all(isinstance(k, str) for k in permitted_set):
        raise ValueError("All entries in PERMITTED_FIELDS must be strings")

    for key, value in details.items():
        if key in permitted_set:
            updated[key] = value

    return updated