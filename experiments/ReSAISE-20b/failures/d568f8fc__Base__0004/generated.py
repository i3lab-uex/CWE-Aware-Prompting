#!/usr/bin/env python3
"""
Utility module for safely updating product data.

The function `adjust_product_data` updates a product dictionary only
for fields explicitly listed in the global ``PERMITTED_FIELDS`` list.
This protects against CWE‑915: improperly controlled modification of
dynamically determined object attributes.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Global configuration: list of fields that are allowed to be modified.
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
def adjust_product_data(prod_info: Dict[str, Any],
                        change_vals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied only to
    permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product dictionary. It is **not** modified in place.
    change_vals : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A shallow copy of ``prod_info`` with the allowed updates applied.

    Raises
    ------
    ValueError
        If ``change_vals`` contains any key that is not in ``PERMITTED_FIELDS``.

    Notes
    -----
    * The function performs a shallow copy of the input dictionary; nested
      objects are not deep‑copied.
    * Keys in ``change_vals`` that are not permitted are ignored, and a
      :class:`ValueError` is raised to notify callers of the misuse.
    """
    # Validate that all requested changes are permitted
    disallowed = set(change_vals) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify non‑permitted fields: {sorted(disallowed)}"
        )

    # Create a shallow copy of the original product to avoid side effects
    updated_product = copy.copy(prod_info)

    # Apply allowed updates
    for key, value in change_vals.items():
        updated_product[key] = value

    return updated_product