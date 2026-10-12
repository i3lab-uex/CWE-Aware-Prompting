#!/usr/bin/env python3
"""
Product update utility.

This module defines a single public function, ``amend_product_features``,
which updates fields of a product dictionary with values supplied in a
payload.  Only keys listed in ``PERMITTED_FIELDS`` are allowed to be
modified; attempting to change any other key results in a ``ValueError``.

The function mutates the supplied product dictionary and also returns it
for convenience.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: list of fields that can be modified by the API.
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update a product dictionary with values from *payload*.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It may contain any keys, but only
        those listed in :data:`PERMITTED_FIELDS` will be updated.
    payload : dict
        Dictionary containing new values for the product.  Only keys that are
        in :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).

    Raises
    ------
    ValueError
        If *payload* contains any keys that are not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function mutates *item* in place.  It also returns the mutated
    dictionary for convenience.
    """
    # Determine which keys in payload are disallowed
    invalid_keys = set(payload) - PERMITTED_FIELDS
    if invalid_keys:
        raise ValueError(
            f"Attempt to modify disallowed fields: {sorted(invalid_keys)}"
        )

    # Apply allowed updates
    for key in PERMITTED_FIELDS:
        if key in payload:
            item[key] = payload[key]

    return item

# --------------------------------------------------------------------------- #
# End of module
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Basic demo / sanity check
    product = {"price": 10.0, "description": "A", "stock": 5, "category": "Tools"}
    new_values = {"price": 12.0, "stock": 4}
    print("Before:", product)
    amended = amend_product_features(product, new_values)
    print("After :", amended)

    # Uncomment to see the error handling
    # bad_payload = {"price": 15, "color": "red"}
    # amend_product_features(product, bad_payload)