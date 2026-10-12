# -*- coding: utf-8 -*-

"""
Product update utility.

This module defines a single function, `update_product_info`, that updates
fields of a product dictionary in place.  Only fields listed in the global
`PERMITTED_FIELDS` list are allowed to be modified.

The implementation is intentionally simple, but it follows best practices
to avoid common pitfalls:

* It operates on a shallow copy of the product to prevent accidental mutation
  of shared references.
* Only permitted keys are updated; any other key in `change_data` is ignored.
* The function returns the modified product dictionary so callers can use
  the updated value immediately.
"""

from typing import Dict, Any

# Define which fields may be updated.  This list should be kept in sync
# with the schema of the product dictionary.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_info(prod: Dict[str, Any],
                        change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update allowed fields of a product dictionary with new values.

    Parameters
    ----------
    prod : dict
        The original product representation.  This dictionary may contain any
        number of keys, but only those listed in `PERMITTED_FIELDS` are
        considered safe to modify.
    change_data : dict
        A dictionary mapping field names to new values.  Keys not present in
        `PERMITTED_FIELDS` are ignored.

    Returns
    -------
    dict
        A new dictionary that contains the original product data with the
        permitted fields updated.  The original `prod` dictionary is left
        unchanged.

    Notes
    -----
    * This function does **not** perform type checking on the values.  It
      simply assigns whatever value is provided for a permitted key.
    * If `change_data` contains keys that are not in the product dictionary
      but are allowed, they will be added.
    """
    # Create a shallow copy to avoid mutating the caller's data
    updated_prod = prod.copy()

    for key, value in change_data.items():
        if key in PERMITTED_FIELDS:
            updated_prod[key] = value
    return updated_prod