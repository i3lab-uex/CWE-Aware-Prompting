# SPDX-License-Identifier: MIT
"""
A simple utility to safely edit product information.
Only the fields defined in `PERMITTED_FIELDS` may be updated.

The implementation follows best practices to avoid CWE‑913
by preventing unintended modification of disallowed attributes.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that are allowed to be modified.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with the values provided in `details`.

    Parameters
    ----------
    item : dict
        The original product data. This dictionary will not be modified.
    details : dict
        Key/value pairs that should be applied to the product. Only keys listed in
        `PERMITTED_FIELDS` are considered.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.

    Raises
    ------
    ValueError
        If `details` contains a key that is not in `PERMITTED_FIELDS`.

    Notes
    -----
    * The function returns a **copy** of the original item, ensuring that the
      caller's data is not mutated.
    * Any attempt to modify a non‑permitted field raises an exception, making
      the behaviour explicit and preventing silent failures.
    """
    # Validate that all keys in `details` are permitted
    for key in details:
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Attempted to modify unpermitted field '{key}'. "
                "Only the following fields are editable: "
                f"{', '.join(PERMITTED_FIELDS)}."
            )

    # Create a deep copy to avoid mutating the original item
    updated_item = deepcopy(item)

    # Apply permitted updates
    for key, value in details.items():
        updated_item[key] = value

    return updated_item