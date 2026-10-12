#!/usr/bin/env python3
"""
Product data modifier.

This module defines a single public function, `modify_product_data`, which updates
a product dictionary only for attributes that are explicitly allowed.  The
`PERMITTED_FIELDS` list is the authoritative source of truth for which fields
may be changed.  All other keys in `update_info` are ignored, and an optional
exception can be raised if strict validation is required.

The implementation avoids the CWE‑915 vulnerability by ensuring that attribute
names are not taken from untrusted input but only from the controlled list.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# List of attributes that may be updated.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_product_data(
    product_details: Dict[str, Any],
    update_info: Dict[str, Any],
    *,
    strict: bool = False,
) -> Dict[str, Any]:
    """
    Update a product dictionary with values from *update_info*.

    Only keys that are present in :data:`PERMITTED_FIELDS` will be applied.
    The function returns a new dictionary; the original *product_details* is
    left unchanged.

    Parameters
    ----------
    product_details:
        The original product data.  Must be a mapping containing any keys
        (e.g., ``price``, ``description``).
    update_info:
        The proposed updates.  Keys that are not in :data:`PERMITTED_FIELDS`
        are ignored unless *strict* is ``True``.
    strict:
        If ``True``, a :class:`ValueError` is raised when *update_info* contains
        any key not in :data:`PERMITTED_FIELDS`.  If ``False`` (the default),
        such keys are silently ignored.

    Returns
    -------
    dict:
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If *strict* is ``True`` and an invalid field is present in
        *update_info*.
    """
    # Make a shallow copy so we don't mutate the caller's dict
    updated_product = copy.deepcopy(product_details)

    # Identify any disallowed keys for reporting/validation
    invalid_keys = [k for k in update_info if k not in PERMITTED_FIELDS]

    if strict and invalid_keys:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(invalid_keys)}"
        )

    # Apply only permitted updates
    for key in PERMITTED_FIELDS:
        if key in update_info:
            updated_product[key] = update_info[key]

    return updated_product