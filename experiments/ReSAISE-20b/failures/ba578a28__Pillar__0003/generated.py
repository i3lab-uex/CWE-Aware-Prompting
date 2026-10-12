# -*- coding: utf-8 -*-
"""
Product data modification module.

This module defines a single public function `modify_product_data` that updates
a product dictionary with values supplied in an update dictionary.  Only the
fields enumerated in `PERMITTED_FIELDS` are allowed to be modified; any other
attempts raise a ValueError.

The function performs defensive copying so that the original product data is
not mutated, preventing accidental side‑effects.  It also validates input
types to guard against malicious or malformed data.

Security note: The implementation deliberately avoids executing arbitrary code
or modifying attributes that could compromise the integrity of the product
representation.  It also follows best practices for handling mutable data,
mitigating potential issues identified in CWE‑664 (Improper Control of a
Resource Through its Lifetime).
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Allowed fields that can be modified.  Add or remove fields here as needed.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def _validate_update_keys(update_info: Dict[str, Any]) -> None:
    """
    Ensure that all keys in update_info are permitted.

    Raises:
        ValueError: If any key is not listed in PERMITTED_FIELDS.
    """
    invalid_keys = set(update_info) - set(PERMITTED_FIELDS)
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {sorted(invalid_keys)}"
        )


def modify_product_data(product_details: Dict[str, Any],
                         update_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted updates applied.

    Parameters
    ----------
    product_details : dict
        The original product data.  Must be a mapping from string keys to any
        JSON‑serialisable values.
    update_info : dict
        Mapping of fields to new values.  Only keys in `PERMITTED_FIELDS`
        are considered; others raise ValueError.

    Returns
    -------
    dict
        A shallow copy of `product_details` with updates applied.

    Raises
    ------
    ValueError
        If ``update_info`` contains keys not in `PERMITTED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Ensure that only permitted fields are updated
    _validate_update_keys(update_info)

    # Create a copy to avoid mutating the caller's data
    updated_product = copy.deepcopy(product_details)

    # Apply updates
    for key, value in update_info.items():
        updated_product[key] = value

    return updated_product