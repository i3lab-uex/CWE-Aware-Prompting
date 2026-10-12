# -*- coding: utf-8 -*-
"""
Utility module for safely updating product dictionaries.

The function `adjust_product_data` updates only fields that are listed in
the global ``PERMITTED_FIELDS`` list.  Any attempt to modify a field that is
not explicitly permitted raises ``ValueError`` to prevent accidental
changes or injection of malicious data.

This module intentionally avoids mutating the input dictionaries directly
unless it is safe to do so.  It returns a new dictionary instance that
represents the updated product, leaving the original untouched to avoid
unintended side‑effects.  This practice mitigates risks such as CWE‑664,
where improper handling of a resource's lifetime can lead to
inconsistent state or leaks.
"""

from __future__ import annotations

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Return a new product dictionary with updates applied only to permitted fields.

    Parameters
    ----------
    prod_info : dict
        Original product data.  Keys represent attributes such as 'price',
        'description', etc.
    change_vals : dict
        Dictionary containing the new values for fields that should be updated.

    Returns
    -------
    dict
        A new dictionary containing the original data with permitted updates applied.

    Raises
    ------
    ValueError
        If ``change_vals`` contains a key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of ``prod_info``.  If the product
      contains nested mutable objects, they will be shared between the original
      and returned dictionary.
    - This implementation is intentionally defensive: it does not allow
      accidental mutation of disallowed keys, protecting against CWE‑664
      style misuse where a resource could be left in an inconsistent state.
    """
    # Validate that all requested changes are permitted
    disallowed = set(change_vals) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Create a shallow copy to avoid mutating the original dictionary
    updated = prod_info.copy()

    # Apply permitted updates
    for key, value in change_vals.items():
        updated[key] = value

    return updated