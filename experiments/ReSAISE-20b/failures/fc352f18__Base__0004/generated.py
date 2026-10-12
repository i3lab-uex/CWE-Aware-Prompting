# SPDX-License-Identifier: MIT
"""
Product feature amendment utility.

This module defines the `amend_product_features` function which updates a
product dictionary with values supplied in a payload.  Only keys that are
present in the globally defined `PERMITTED_FIELDS` list may be modified.
Attempting to modify any other key raises a ``ValueError`` to prevent
unintended or malicious changes.

The function performs a shallow copy of the original product dictionary,
applies permitted updates, and returns the updated copy.  The original
dictionary remains unchanged.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Global list of fields that may be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]


def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update the given product dictionary with values from ``payload``.
    
    Only keys listed in :data:`PERMITTED_FIELDS` are allowed to be updated.
    Any attempt to modify other keys results in a ``ValueError``.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It may contain any keys.
    payload : dict
        Dictionary containing new values for the product fields.

    Returns
    -------
    dict
        A shallow copy of ``item`` with the permitted fields updated.

    Raises
    ------
    ValueError
        If ``payload`` contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    # Create a shallow copy to avoid mutating the caller's data.
    updated_item = item.copy()

    for key, value in payload.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Attempted to modify forbidden field '{key}'. "
                f"Only the following fields are allowed: {PERMITTED_FIELDS}"
            )
        updated_item[key] = value

    return updated_item