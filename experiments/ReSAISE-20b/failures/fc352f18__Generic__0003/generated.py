# SPDX-License-Identifier: MIT
"""
Utility module for safely updating product dictionaries.
"""

from __future__ import annotations

# List of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update the fields of a product dictionary with values from *payload*.

    Only keys that appear in :data:`PERMITTED_FIELDS` are accepted.
    Any attempt to modify a disallowed field raises ``ValueError``.

    Parameters
    ----------
    item : dict
        The original product dictionary. It is modified in place.
    payload : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated product dictionary (the same object as *item*).

    Raises
    ------
    ValueError
        If *payload* contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    # Ensure payload only contains allowed keys
    disallowed = set(payload) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Perform the updates
    for key, value in payload.items():
        item[key] = value

    return item