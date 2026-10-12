#!/usr/bin/env python3
"""
Secure product information updater.

This module defines a single public function `update_item_information` that
updates a product dictionary with new values provided in another dictionary.
Only attributes listed in the global `PERMITTED_FIELDS` constant are allowed to
be modified. Any attempt to modify a non‑permitted attribute is silently
ignored, and the function never alters keys that are not explicitly permitted.

The implementation guards against common dynamic attribute modification
vulnerabilities (CWE‑915) by validating keys and ensuring the input dictionaries
are plain `dict` instances.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration: fields that may be updated by `update_item_information`.
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS = {
    "price",
    "description",
    "stock",
    "category",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def update_item_information(
    product_info: Dict[str, Any], new_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied only to
    permitted fields.

    Parameters
    ----------
    product_info : dict
        Original product attributes. Must be a plain dictionary.
    new_data : dict
        Proposed updates. Only keys present in `PERMITTED_FIELDS` will be
        applied.

    Returns
    -------
    dict
        A new dictionary representing the updated product state. The input
        dictionaries are left untouched.

    Raises
    ------
    TypeError
        If either argument is not a dictionary instance.
    """

    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Work on a deep copy to avoid mutating the original data.
    updated_product = deepcopy(product_info)

    for key, value in new_data.items():
        # Ensure the key is a string and permitted.
        if isinstance(key, str) and key in PERMITTED_FIELDS:
            updated_product[key] = value
        else:
            # Silently ignore disallowed or non-string keys.
            continue

    return updated_product