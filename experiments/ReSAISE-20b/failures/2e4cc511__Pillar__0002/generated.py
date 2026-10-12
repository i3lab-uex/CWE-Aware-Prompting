# frozen_string_literal: true

from __future__ import annotations

import copy
from typing import Dict, Any

# Only these keys may be updated.  Anything else is rejected.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def update_item_details(
    inventory: Dict[str, Any], update_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update the supplied `inventory` dictionary with values from `update_data`
    only for keys listed in ``PERMITTED_FIELDS``.  The function returns a
    **new** dictionary containing the updated product information, leaving
    the original ``inventory`` unchanged.

    Parameters
    ----------
    inventory : dict
        The original product dictionary.  It may contain arbitrary keys,
        but only the permitted ones will be modified.
    update_data : dict
        Dictionary containing keys and values that should be applied to the
        product.

    Returns
    -------
    dict
        A new dictionary with permitted updates applied.  If no changes are
        made the original inventory is returned unchanged.

    Raises
    ------
    ValueError
        If ``update_data`` contains keys that are not in ``PERMITTED_FIELDS``.
    TypeError
        If either argument is not a mapping type.

    Notes
    -----
    * The function performs a shallow copy of the original inventory to avoid
      accidental mutation of shared objects.
    * This implementation is intentionally straightforward; it does not
      perform type validation on the values themselves, as that would be
      product‑specific.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a mapping type (dict).")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a mapping type (dict).")

    # Validate keys
    invalid_keys = set(update_data) - PERMITTED_FIELDS
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {sorted(invalid_keys)}"
        )

    # Create a shallow copy to avoid side effects
    updated = copy.deepcopy(inventory)

    # Apply updates
    for key, value in update_data.items():
        updated[key] = value

    return updated