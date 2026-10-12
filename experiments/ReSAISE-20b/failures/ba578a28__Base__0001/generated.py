# -*- coding: utf-8 -*-
"""
Utility for safely updating product dictionaries.

The module defines a single public function `modify_product_data` that updates
a product dictionary only for attributes explicitly listed in the global
``PERMITTED_FIELDS`` list.  This protects against CWE-915 (improperly
controlled modification of dynamically‑determined object attributes).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration: only these fields may be updated.
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_product_data(
    product_details: dict,
    update_info: dict
) -> dict:
    """
    Update a product dictionary with values from ``update_info`` only for
    fields that are present in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product_details : dict
        The original product dictionary.  It will be updated in place and also
        returned.
    update_info : dict
        A dictionary containing key/value pairs that should be applied to the
        product.  Only keys present in :data:`PERMITTED_FIELDS` are honored.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    KeyError
        If ``update_info`` contains a key that is not in :data:`PERMITTED_FIELDS`.
    TypeError
        If ``product_details`` or ``update_info`` is not a mapping type.

    Notes
    -----
    The function modifies ``product_details`` in place to avoid creating a new
    object.  This behaviour is documented and intentional; callers who need a
    copy should explicitly create one before calling this function.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a mapping type (dict).")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a mapping type (dict).")

    # Validate keys first to provide an atomic operation.
    invalid_keys = set(update_info) - PERMITTED_FIELDS
    if invalid_keys:
        raise KeyError(
            f"Attempted to update disallowed fields: {sorted(invalid_keys)}"
        )

    # Perform the updates.
    product_details.update(update_info)
    return product_details