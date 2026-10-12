# -*- coding: utf-8 -*-
"""
Utility module for product updates.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that are allowed to be updated.  This list is deliberately kept
# small to reduce the attack surface and prevent accidental changes to
# sensitive fields such as `id`, `created_at`, or other system managed keys.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values.

    Parameters
    ----------
    prod : dict
        Original product representation.  The dictionary is **not** modified in place;
        a shallow copy is returned.
    change_data : dict
        Dictionary containing the new values for fields that should be updated.

    Returns
    -------
    dict
        A new dictionary containing the merged product information.
        Fields not listed in ``PERMITTED_FIELDS`` are ignored.

    Raises
    ------
    ValueError
        If ``change_data`` contains keys that are not in ``PERMITTED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    This function guards against CWE-664 by ensuring that only explicitly allowed
    fields are updated.  No external resources (e.g., file handles, database
    connections) are touched; the function purely operates on in‑memory data.
    """
    if not isinstance(prod, dict):
        raise TypeError("prod must be a dictionary")
    if not isinstance(change_data, dict):
        raise TypeError("change_data must be a dictionary")

    # Create a shallow copy to avoid side‑effects on the caller's object.
    updated = copy.deepcopy(prod)

    # Track any disallowed keys for reporting.
    invalid_keys = [k for k in change_data if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"The following keys are not permitted to be updated: {', '.join(invalid_keys)}"
        )

    # Apply updates.
    for key, value in change_data.items():
        updated[key] = value

    return updated