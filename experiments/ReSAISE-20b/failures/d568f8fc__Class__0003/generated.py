# -*- coding: utf-8 -*-

"""
Product data adjustment module.

This module provides a single public function, ``adjust_product_data``, which
updates an existing product dictionary with new values while strictly
controlling which fields may be modified.  The list of modifiable keys is
defined by the global ``PERMITTED_FIELDS`` variable.

Security note:
  * Only keys present in ``PERMITTED_FIELDS`` are accepted.
  * No arbitrary code execution or dynamic attribute manipulation is performed.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
#  Configuration
# --------------------------------------------------------------------------- #

# Define the set of fields that may be updated.  Add or remove keys as needed.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def adjust_product_data(prod_info: Dict[str, Any], change_vals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values while enforcing field permissions.

    Parameters
    ----------
    prod_info : dict
        The original product data.  This dictionary will **not** be modified.
    change_vals : dict
        Mapping of field names to new values that should replace the current ones.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If ``change_vals`` contains a key that is not listed in
        :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function performs a shallow copy of ``prod_info`` before applying changes,
    so the original dictionary remains untouched.  The returned dictionary may
    share nested mutable objects with ``prod_info`` (e.g., lists or dicts inside the
    product).  For a deep copy, use :func:`copy.deepcopy` on the result if needed.
    """
    # Validate input types
    if not isinstance(prod_info, dict):
        raise TypeError(f"prod_info must be a dict, got {type(prod_info).__name__}")
    if not isinstance(change_vals, dict):
        raise TypeError(f"change_vals must be a dict, got {type(change_vals).__name__}")

    # Convert permitted fields to a set for fast membership checks
    allowed = set(PERMITTED_FIELDS)

    # Check that all keys in change_vals are permitted
    disallowed = set(change_vals) - allowed
    if disallowed:
        raise ValueError(
            f"The following fields are not permitted for update: {sorted(disallowed)}"
        )

    # Create a shallow copy of the original product data
    updated_product = copy.deepcopy(prod_info)

    # Apply allowed changes
    for key, value in change_vals.items():
        updated_product[key] = value

    return updated_product