# SPDX-License-Identifier: MIT

"""
Utility for safely updating product data.

The module defines a single public function `adjust_product_data` that
updates only fields listed in the global `PERMITTED_FIELDS`.  All other
attempts to modify the product are ignored, protecting against
unintended or malicious changes.

Author: ChatGPT
"""

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product data.  This dictionary is not modified in place;
        a new dictionary containing the updates is returned.
    change_vals : dict
        Dictionary of fields to update.  Only keys present in
        ``PERMITTED_FIELDS`` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.  The original
        ``prod_info`` remains unchanged.

    Notes
    -----
    - Fields not in ``PERMITTED_FIELDS`` are silently ignored.
    - The function performs a shallow copy of ``prod_info`` to avoid
      side‑effects on the caller's data.
    """
    # Create a shallow copy to avoid mutating the original product.
    updated_product = prod_info.copy()

    # Iterate over requested changes and apply only permitted ones.
    for field, new_value in change_vals.items():
        if field in PERMITTED_FIELDS:
            updated_product[field] = new_value

    return updated_product