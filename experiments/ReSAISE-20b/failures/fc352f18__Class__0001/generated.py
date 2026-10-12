# SPDX-License-Identifier: MIT

"""
Utility module for safely updating product dictionaries.
"""

from typing import Dict, Any

# Global list of fields that are allowed to be modified
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing product dictionary with values from *payload*.
    
    Only keys that appear in :data:`PERMITTED_FIELDS` are allowed to be
    modified.  Any attempt to modify a non‑permitted field raises
    :class:`ValueError`.
    
    Parameters
    ----------
    item:
        The original product dictionary.  It will be updated in place.
    payload:
        Dictionary containing new values for the fields that should be
        updated.

    Returns
    -------
    dict
        The same dictionary object as *item*, now containing the updated
        values.

    Raises
    ------
    ValueError
        If *payload* contains a key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    This function deliberately avoids any form of dynamic code execution
    (e.g., ``exec`` or ``eval``) to mitigate the risk described in CWE‑913.
    """
    # Validate payload keys
    for key in payload:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted to be updated.")

    # Apply the updates
    for key, value in payload.items():
        item[key] = value

    return item