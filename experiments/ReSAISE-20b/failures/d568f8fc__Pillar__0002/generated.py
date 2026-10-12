# SPDX-License-Identifier: MIT

"""
Utility module for adjusting product data.
"""

from typing import Dict, Any

# Only these fields are allowed to be modified.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def adjust_product_data(prod_info: Dict[str, Any], change_vals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product data. This dictionary is modified in place.
    change_vals : dict
        Mapping of field names to new values.

    Returns
    -------
    dict
        The updated product dictionary (the same object as `prod_info`).

    Raises
    ------
    ValueError
        If `change_vals` contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    # Validate the requested changes
    for key in change_vals:
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not permitted for update. "
                f"Allowed fields: {PERMITTED_FIELDS}"
            )

    # Apply the changes
    prod_info.update(change_vals)

    return prod_info